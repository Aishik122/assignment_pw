from flask import Flask, request, render_template,redirect
import pandas as pd
from src.component.data_ingestion import DataIngestion


# preview Data 
df=pd.read_csv(r'artifacts\raw_data.csv',encoding="unicode_escape")
headers = df.columns 
records = df.to_records(index=False)
result = list(records)


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
def amazom_data():
    return render_template('amazon.html',headings = headers , data = result )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)