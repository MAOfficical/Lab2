import streamlit as st
import requests


def get_weather_data(lat, lon):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = 'YOUR_API_KEY'
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    
    weather_response = requests.get(weather_url).json()
    air_quality_response = requests.get(air_quality_url).json()
    
    # Extracting relevant data
    temperature = weather_response.get("main", {}).get("temp")
    humidity = weather_response.get("main", {}).get("humidity")
    aqi = air_quality_response.get("list", [{}])[0].get("main", {}).get("aqi")
    
    return temperature, humidity, aqi
