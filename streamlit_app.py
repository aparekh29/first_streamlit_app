import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # streamlit.text(fruityvice_response.json())
    # Normalize json to rows and columns.
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # Dispplay the normalized data.
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# Allow user to add fruit to the list.
add_my_fruit = streamlit.text_input('What fruit would you like to add ?')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute( "insert into fruit_load_list values ( 'from streamlit' )" )
