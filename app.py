from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

API_KEY = '878fd1c5e3e6a55130a0183148c35409'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    city = ''

    if request.method == 'POST':
        city = request.form['city']
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        if response.get('cod') == 200:
            weather_data = {
                'city': response['name'],
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'].title(),
                'icon': response['weather'][0]['icon'],
                'humidity': response['main']['humidity'],
                'wind_speed': response['wind']['speed']
            }
        else:
            weather_data = {'error': 'City not found. Please try again.'}

    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <title>City Weather</title>
            <style>
              body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(to right, lightskyblue, lightcyan);
                color: black;
                margin: 0;
                font-size: 22px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
              }
              h1 {
                font-size: 40px;
                text-shadow: 1px 1px 2px gray;
                margin-bottom: 20px;
              }
              h1 a {
                color: inherit;
                text-decoration: none;
              }
              h1 a:hover {
                text-decoration: underline;
              }
              form {
                text-align: center;
                margin-bottom: 20px;
              }
              input {
                padding: 14px;
                width: 280px;
                border-radius: 8px;
                border: 1px solid lightgray;
                font-size: 18px;
                box-shadow: 0 2px 5px lightgray;
              }
              button {
                padding: 14px 20px;
                border-radius: 8px;
                border: none;
                background-color: limegreen;
                color: white;
                font-size: 18px;
                margin-left: 10px;
                cursor: pointer;
                transition: background-color 0.3s;
              }
              button:hover {
                background-color: forestgreen;
              }
              .weather-info {
                margin-top: 30px;
                font-size: 24px;
                text-align: center;
                background: white;
                padding: 20px 30px;
                border-radius: 12px;
                box-shadow: 0 4px 10px gray;
                max-width: 400px;
              }
              .weather-info img {
                margin: 10px 0;
              }
            </style>
        </head>
        <body>
            <h1><a href="/">🌤 City Weather 🌤</a></h1>
            <form method="POST">
                <input type="text" name="city" placeholder="Enter City Name" required>
                <button type="submit">Search</button>
            </form>

            {% if weather_data %}
                <div class="weather-info">
                {% if weather_data.error %}
                    <p>{{ weather_data.error }}</p>
                {% else %}
                    <h2 style="font-size:32px;">{{ weather_data.city }}</h2>
                    <p><strong style="font-size:30px;">{{ weather_data.temperature }}°C</strong></p>
                    <p>{{ weather_data.description }}</p>
                    <img src="https://openweathermap.org/img/wn/{{weather_data.icon}}@2x.png">
                    <p>Humidity: {{ weather_data.humidity }}%</p>
                    <p>Wind Speed: {{ weather_data.wind_speed }} m/s</p>
                {% endif %}
                </div>
            {% endif %}
        </body>
        </html>
    ''', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)