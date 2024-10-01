from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Use your actual API key here or set it via environment variables.
API_KEY = 'your_weatherapi_key'  # Replace with your actual WeatherAPI key

# Function to get weather data from WeatherAPI.com
def get_weather_data(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no'
    response = requests.get(url)
    data = response.json()
    return data

# Function to predict energy source
def predict_energy_source(weather_data, is_near_water=False, is_geothermal_region=False):
    wind_speed = weather_data['current']['wind_kph'] * 0.27778  # Convert kph to m/s
    sunlight_hours = 6  # This can be assumed or fetched dynamically from another API
    rainfall = weather_data['current'].get('precip_mm', 0)  # Get rainfall in mm
    condition = weather_data['current']['condition']['text']  # Weather condition

    # Example logic to predict energy source based on weather conditions
    if sunlight_hours > 5:
        return "Solar Energy"
    elif wind_speed > 10:
        return "Wind Energy"
    elif is_near_water and rainfall > 50:
        return "Hydropower"
    elif is_geothermal_region:
        return "Geothermal Energy"
    else:
        return "No optimal renewable energy source found"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    city = request.form['city']
    is_near_water = request.form.get('is_near_water') == 'on'
    is_geothermal_region = request.form.get('is_geothermal_region') == 'on'

    # Get the weather data for the specified city
    weather_data = get_weather_data(city)

    # Predict the energy source based on the weather and geographical data
    energy_source = predict_energy_source(weather_data, is_near_water, is_geothermal_region)
    
    return jsonify({'energy_source': energy_source})

if __name__ == '__main__':
    app.run(debug=True)
