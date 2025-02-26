from flask import Flask, render_template
import requests

app = Flask(__name__)

def fetch_latest_wind_data():
    url = "https://www.met.ie/Open_Data/json/dublin_airport.json"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    stations = data.get("stations", [])
    if not stations:
        return None, None

    station = stations[0]
    time_items = station.get("timeseries", {}).get("timeItems", [])
    if not time_items:
        return None, None

    latest_observation = time_items[-1]
    weather_parameters = latest_observation.get("weatherparameters", [])

    wind_speed = None
    wind_direction = None

    for param in weather_parameters:
        if "Wind speed [m/s]" in param:
            wind_speed = param["Wind speed [m/s]"]
        if "Wind direction [deg]" in param:
            wind_direction = param["Wind direction [deg]"]

    return wind_speed, wind_direction

def kayaking_decision(wind_speed, wind_direction):
    if wind_direction is None or wind_speed is None:
        return "NO DATA", "status-nogo", "No wind data available"

    if 0 <= wind_direction < 180:
        # Northerly winds
        if wind_speed < 12:
            return "GO", "status-go", "Northerly winds < 12 m/s"
        else:
            return "NO GO", "status-nogo", "Northerly winds ≥ 12 m/s"
    elif 180 <= wind_direction <= 360:
        # Southerly winds
        if wind_speed < 9:
            return "GO", "status-go", "Southerly winds < 9 m/s"
        else:
            return "NO GO", "status-nogo", "Southerly winds ≥ 9 m/s"
    else:
        return "NO DATA", "status-nogo", "Invalid wind direction"

@app.route('/')
def home():
    wind_speed, wind_direction = fetch_latest_wind_data()
    status, status_class, decision_rule = kayaking_decision(wind_speed, wind_direction)

    return render_template('index.html',
                           status=status,
                           status_class=status_class,
                           wind_speed=wind_speed if wind_speed is not None else "N/A",
                           wind_direction=wind_direction if wind_direction is not None else "N/A",
                           decision_rule=decision_rule)

if __name__ == '__main__':
    app.run(debug=True)
