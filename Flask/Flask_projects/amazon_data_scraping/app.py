from flask import Flask,request , render_template
import requests
from src.component import data_ingestion 

app = Flask(__name__)

@app.route('/home',methods=['GET','POST'])
def Hellow_world():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        URL= requests.form.get('data-url')
        df=data_ingestion()
        final_df=df.web_scrap()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)



