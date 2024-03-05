from flask import Flask,request , render_template
import requests
from src.component.data_ingestion import  DataIngestion
from src.logger import logging

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/process_link', methods=['POST'])
def process_link():
    link = request.form['link']
    # Do something with the link, for example, print it
    alpha = DataIngestion()
    alpha.web_scrap(url=link,nums_page=2)

    return render_template('PleaseWait.html')

@app.route('/process_completed')
def project_complete():
    return render_template('file generated in artefacts folder')

    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)



