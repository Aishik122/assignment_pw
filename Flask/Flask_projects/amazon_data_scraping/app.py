from flask import Flask, request, render_template,redirect
import pandas as pd
from src.component.data_ingestion import DataIngestion

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/process_link', methods=['POST', 'GET'])
def process_link():
    if request.method == 'POST':
        link = request.form.get('link')
        if link:
            # Process the link and save the data to artifacts folder
            alpha = DataIngestion()
            alpha.web_scrap(url=link, nums_page=2)
            # Redirect to another route or render a template
            return render_template('/home.html')
    # If no link is provided or it's a GET request, redirect to the home page
    return render_template('/home.html')


@app.route('/amazon')
def amazon():
    amazon_data = read_amazon_data()
    return render_template('amazon.html', amazon_data=amazon_data)

def read_amazon_data():
    # Read the CSV file
    amazon_data = pd.read_csv(r'\artifacts\raw_data.csv')
    return amazon_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)