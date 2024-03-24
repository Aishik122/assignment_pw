from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=kolkata&unit=metric&appid=ee31290b9b49856f1ad681ed5ae94773')
    data = response.json()

    # Extract relevant information from the API response
    weather = {
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description']
    }

    # Render the template with weather data
    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)