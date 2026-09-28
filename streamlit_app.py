# Import python packages
import streamlit as st
cnx=st.connection('snowflake')
session = cnx.session()
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Custoize Your Smoothie: {st.__version__}")
st.write(
 "Choos the fruits you want in your custome Smoothie"
)


name_on_order=st.text_input('Name On Smoothie:')
st.write('The name on your Smoothie will be:',name_on_order)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect('Choose upto 5 fruits:',my_dataframe,max_selections=5)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredient_string=''
    for x in ingredients_list:
        ingredient_string+=x+' '

    st.write(ingredient_string)

    my_insert_stmt = """insert into smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
    values ('""" + ingredient_string + """', '""" + name_on_order + """')"""
    st.write(my_insert_stmt)
    

    time_to_insert=st.button('Submit')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
import requests

smoothiefruit_response = requests.get(
"https://www.smoothiefroot.com/api/fruit/watermelon")

#st.text(smoothiefruit_response.json())
sf_df=st.dataframe(data=smoothiefruit_response.json(),use_container_width=True)
