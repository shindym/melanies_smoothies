# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)

# Write directly to the app
name_on_order = st.text_input("Name on smoothie")
st.write("The current name on the smoothie is", name_on_order)

st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingrediants = st.multiselect(
    "What are your favorite colors",my_dataframe,max_selections=5)

if ingrediants:
    st.write("You selected:", ingrediants)
    ingredients_string = ''
    for fruit in ingrediants:
        ingredients_string+=fruit + ' '
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order+ """')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
