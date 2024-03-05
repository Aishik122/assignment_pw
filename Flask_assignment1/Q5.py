from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import os 


app = Flask(__name__)
app.secret_key = os.urandom(24)  


class CustomData:
    def __init__(self, name: str, age: int, roll: str, course: str):
        self.name = name
        self.age = age
        self.roll = roll
        self.course = course
        
    def get_data_frame(self):
        try:
            custom_data_input_dict = {
                'name': [self.name],
                'age': [self.age],
                'roll': [self.roll],
                'course': [self.course]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise Exception()

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        data = CustomData(
            name=request.form.get('name'),
            age=request.form.get('age'),
            roll=request.form.get('roll'),
            course=request.form.get('course')
        )
        df = data.get_data_frame()

        # Store user data in the session
        session['user_data'] = df.to_dict(orient='records')[0]

        return redirect(url_for('index'))  # Change to 'index' instead of 'submit'

@app.route('/index')  # Change from '/submit' to '/index'
def index():
    # Retrieve user data from the session
    user_data = session.get('user_data', None)

    if user_data:
        return render_template('index.html', name=user_data['name'], age=user_data['age'],
                               roll=user_data['roll'], course=user_data['course'])
    else:
        return "Data not available yet"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)