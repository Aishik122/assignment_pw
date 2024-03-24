from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=kolkata&unit=metric&appid=ee31290b9b49856f1ad681ed5ae94773')
    data = response.json()

    # Render the template with weather data
    return render_template('index.html', weather_data=data)

if __name__ == '__main__':
    app.run(debug=True)
