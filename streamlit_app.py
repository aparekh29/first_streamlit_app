import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data( this_fruit_choice ):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # Normalize json to rows and columns.
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute( "select * from fruit_load_list" )
        return my_cur.fetchall()

def insert_row_snowflake( new_fruit ):
    with my_cnx.cursor() as my_cur:
        my_cur.execute( "insert into fruit_load_list values ('" + new_fruit + "')")
        return "Thanks for adding " + new_fruit

streamlit.title("My Parents New Healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 and Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach and Rocket Smoothie")
streamlit.text("🐔 Hard-boiled and Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv( 'https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt' )
my_fruit_list = my_fruit_list.set_index("Fruit")

# Let's put a multi-select here so that user can pick the fruit he/she likes.
fruits_selected = streamlit.multiselect( "Pick some fruit" , list( my_fruit_list.index ) , [ 'Avocado' , 'Strawberries' ] )
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the dataframe on the webpage.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice !")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
    streamlit.write('The user entered ', fruit_choice)
  else:
    fruityvice_normalized = get_fruityvice_data( fruit_choice )
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

streamlit.header("View Our Fruit List - Add Your Favorites !")
if streamlit.button( "Get Fruit list" ):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

# Allow user to add fruit to the list.
add_my_fruit = streamlit.text_input('What fruit would you like to add ?')
if streamlit.button("Add a Fruit to the list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)


