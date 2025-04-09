# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched


helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")

#session = get_active_session()

session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").select(col("ORDER_FILLED"), col('NAME_ON_ORDER'), col('INGREDIENTS'), col('ORDER_TS'), col('ORDER_UID'))
#st.dataframe(data=my_dataframe, use_container_width=True)
editable_df = st.data_editor(my_dataframe)
submitted = st.button('Submit')


if my_dataframe.count()>0:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')

    if submitted:
        st.success("Someone clicked the button.", icon="👍")
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset, (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})])

        except:
            st.write('Something went wrong.')
else:
    st.success('There are no pending orders right now', icon="👍")        
