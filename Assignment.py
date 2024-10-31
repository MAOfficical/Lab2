import streamlit as st
import requests
from streamlit_folium import folium_static
import folium

# Replace with your actual API key
api_key = "include your api key here"

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")

# Cache the map creation function to improve performance
@st.cache_data
def map_creator(latitude, longitude):
    # Initialize the map centered on the given coordinates
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    # Add a marker for the specified location
    folium.Marker([latitude, longitude], popup="Selected Location", tooltip="Location").add_to(m)
    # Display the map in Streamlit
    folium_static(m)

@st.cache_data
def generate_list_of_countries():
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    return countries_dict

@st.cache_data
def generate_list_of_states(country_selected):
    states_url = f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
    states_dict = requests.get(states_url).json()
    return states_dict

@st.cache_data
def generate_list_of_cities(state_selected, country_selected):
    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
    cities_dict = requests.get(cities_url).json()
    return cities_dict

# Category selection: Choose a location method
category = st.selectbox("Choose location method", ["By City, State, and Country", "By Nearest City (IP Address)", "By Latitude and Longitude"])

if category == "By City, State, and Country":
    countries_dict = generate_list_of_countries()
    if countries_dict["status"] == "success":
        countries_list = [i["country"] for i in countries_dict["data"]]
        countries_list.insert(0, "")
        country_selected = st.selectbox("Select a country", options=countries_list)

        if country_selected:
            states_dict = generate_list_of_states(country_selected)
            if states_dict["status"] == "success":
                states_list = [i["state"] for i in states_dict["data"]]
                states_list.insert(0, "")
                state_selected = st.selectbox("Select a state", options=states_list)

                if state_selected:
                    cities_dict = generate_list_of_cities(state_selected, country_selected)
                    if cities_dict["status"] == "success":
                        cities_list = [i["city"] for i in cities_dict["data"]]
                        cities_list.insert(0, "")
                        city_selected = st.selectbox("Select a city", options=cities_list)

                        if city_selected:
                            aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
                            aqi_data_dict = requests.get(aqi_data_url).json()

                            if aqi_data_dict["status"] == "success":
                                data = aqi_data_dict["data"]["current"]
                                temperature = data["weather"]["tp"]
                                humidity = data["weather"]["hu"]
                                aqi = data["pollution"]["aqius"]
                                latitude = data["location"]["coordinates"][1]
                                longitude = data["location"]["coordinates"][0]
                                
                                st.write(f"Temperature: {temperature}°C")
                                st.write(f"Humidity: {humidity}%")
                                st.write(f"Air Quality Index (AQI): {aqi}")
                                map_creator(latitude, longitude)
                            else:
                                st.warning("No data available for this location.")
                    else:
                        st.warning("No cities available. Please select another state.")
            else:
                st.warning("No states available. Please select another country.")
    else:
        st.error("API request limit reached. Wait for a few minutes before your next request.")

elif category == "By Nearest City (IP Address)":
    url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
    aqi_data_dict = requests.get(url).json()

    if aqi_data_dict["status"] == "success":
        data = aqi_data_dict["data"]["current"]
        temperature = data["weather"]["tp"]
        humidity = data["weather"]["hu"]
        aqi = data["pollution"]["aqius"]
        latitude = data["location"]["coordinates"][1]
        longitude = data["location"]["coordinates"][0]
        
        st.write(f"Temperature: {temperature}°C")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Air Quality Index (AQI): {aqi}")
        map_creator(latitude, longitude)
    else:
        st.warning("No data available for this location.")

elif category == "By Latitude
