import streamlit
import pandas

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
streamlit.multiselect( "Pick some fruit" , list( my_fruit_list.index ) )

# Display the dataframe on the webpage.
streamlit.dataframe(my_fruit_list)
