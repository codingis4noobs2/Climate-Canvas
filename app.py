# Import required libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from custom_connection import OpenWeatherApiConnection


st.set_page_config(page_title="Climate Canvas")

st.title("Climate Canvas")
st.subheader("A Weather Visualization Tool")
st.write("Visualize weather data from OpenWeather API")

# Set API key and create API connection
api_key = st.secrets['API_KEY']
conn = st.experimental_connection(
    "openweather-api", type=OpenWeatherApiConnection, api_key=api_key)

# Initialize DataFrame to store weather data
data = pd.DataFrame(columns=["city_name", "temperature", "humidity", "wind_speed"])

# Store DataFrame in session state if not already present
if 'df' not in st.session_state:
    st.session_state.df = data

def get_data():
    """Fetches weather data for a given city name and updates the DataFrame in session state"""
    if name_input != '':
        # Check if limit of 10 cities has been reached
        if len(st.session_state.df) >= 10:
            st.warning('You have reached the maximum limit of 10 cities.')
            return
        # Check if data for city is already in table
        elif name_input in st.session_state.df['city_name'].values:
            st.warning(f'Weather data for {name_input} is already in the table.')
            return
        # Fetch weather data for city
        else:
            data = conn.get_weather_by_city_name(name_input)
            if data is None:
                st.warning(f"No weather data found for city: {name_input}")
            else:
                # Convert temperature from Kelvin to Celsius
                temp_celsius = data['main']['temp'] - 273.15
                new_row = {
                    'city_name': name_input,
                    'temperature': temp_celsius,
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                }
                new_df = pd.DataFrame([new_row])
                st.session_state.df = pd.concat(
                    [st.session_state.df, new_df], ignore_index=True)
                st.session_state['input'] = ""


# Define Streamlit widgets
name_input = st.text_input("Enter a city name:", key='input')
button_clicked = st.button("Submit", on_click=get_data)

# Define plotting feature selection
plot_type = st.selectbox(
    "Select a weather factor to plot:",
    ('temperature', 'humidity', 'wind_speed')
)

# Define units for each weather factor
units = {
    'temperature': '°C',
    'humidity': '%',
    'wind_speed': 'm/s'
}

# Plot data if DataFrame is not empty
if not st.session_state.df.empty:
    st.dataframe(st.session_state.df)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=st.session_state.df, x='city_name', y=plot_type, alpha=0.5, ax=ax, label=plot_type)
    ax.set_xticklabels(st.session_state.df['city_name'], rotation=45)

    st.pyplot(fig)
    st.write(f"*Bar shows {plot_type} in {units[plot_type]}")

    def clear_all():
        """Clears all fetched data from the session state"""
        st.session_state["df"] = data
        st.session_state['input'] = ""

    # Define reset button
    button = st.button("Reset", on_click=clear_all)
