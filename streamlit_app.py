# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f" :cup_with_straw: Customize your smoothie ! :cup_with_straw:")
st.write(
  """Choose the fruit you want in yoour smoothie!
  """
)



name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on your Smoothie will be:",name_on_order)

cnx=st.connection("Snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect('Choose up to 5 Ingredients:',my_dataframe,max_selections=5)

st.write(ingredients_list)
st.text(ingredients_list)

if ingredients_list:
    

    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
		st.subheader(fruit_chosen + 'Nutrition Information')
		smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
		sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)


        
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
        values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)


    #if ingredients_string:
        #session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")

    time_to_insert = st.button('Submit Order')
    if time_to_insert :

        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon="✅")
      
import requests

 
