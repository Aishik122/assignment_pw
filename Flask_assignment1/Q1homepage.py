from flask import Flask 
app = Flask(__name__)
@app.route('/home')
def first_com():
    return "Hellow, World"

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
