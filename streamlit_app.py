# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write("Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:")
st.write("""Choose the fruits you want in your custom Smoothie!""")


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie is:', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()


ingredients_list = st.multiselect(
    'Choose up to 5 indgredients:'
    , my_dataframe
    , max_selections=5
)
if ingredients_list:
    ingredients_string = ''

    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data-smoothiefroot_response.json(), use_container_width=True)

   # st.text(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered!', icon="✅")





