# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customize your smoothie! 🥤")
st.write(
    """Choose the fruit you want in your smoothie!"""
)

# Get smoothie name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on your Smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("Snowflake")
session = cnx.session()

# Fetch available fruits
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
ingredients_list = st.multiselect('Choose up to 5 Ingredients:', my_dataframe, max_selections=5)
st.write(ingredients_list)
st.text(ingredients_list)

#Convert snowpark df to pandas df so we can use LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
#st.stop()


# Process smoothie order
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # Get nutrition info from API
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Show ingredients string
    st.write(ingredients_string)

    # Prepare insert SQL
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """
    st.write(my_insert_stmt)

    # Submit button
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
