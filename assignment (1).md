Q: How would you create a basic Flask route that displays "Hello, World!" on the homepage?
ans:-  ```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

4. **Return a response:** After processing the form data, you can return a response to the user. This could be a simple message indicating success, or it could be a redirect to another page.
```python
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        # Process the form data here
        return 'Name: {}, Email: {}'.format(name, email)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```
This example defines a route `'/'` that handles both GET and POST requests. If the request method is POST, it will retrieve the values from the form using the `request.form` object. You can then process these values as needed and send a response. If the request method is GET, it will render the template `index.html`, which should contain the form for submission.

Q: Write a Flask route that accepts a parameter in the URL and displays it on the page.
ans:- ```python
from flask import Flask

app = Flask(__name__)

@app.route('/<name>')
def hello_name(name):
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(debug=True)
```
This code defines a route with a variable part `/<name>`. When a request is made to this route, the value of `name` in the URL will be passed to the `hello_name` function. The function then uses the value of `name` to construct the message and return it as a response.

Q: Describe the process of connecting a Flask app to a SQLite database using SQLAlchemy.
ans:-  You can connect a Flask app to a SQLite database using SQLAlchemy by following these steps:
1. **Install SQLAlchemy:** Install SQLAlchemy using `pip install SQLAlchemy`.
2. **Configure database connection:** Create a `database.py` module to define your database connection:
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database path
DATABASE_URL = "sqlite:///your_database.db"

# Create the engine
engine = create_engine(DATABASE_URL)

# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base model
Base = declarative_base()

# Function to create a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
3. **Define database models:** Define the structure of your data using SQLAlchemy models:
```python
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```
4. **Initialize the database:** Create the database tables by calling the `Base.metadata.create_all(engine)` function. You can do this in your app's initialization script or in a separate setup function.
5. **Use database operations in your Flask routes:** In your Flask routes, use `get_db()` to get a database session. You can then use this session to perform database operations like creating, reading, updating, and deleting records.
```python
from flask import Flask
from .database import get_db

app = Flask(__name__)

@app.get("/users")
def get_users():
    db = get_db()
    users = db.query(User).all()
    return [user.name for user in users]
```
This example defines a route that fetches all users from the database and returns their names.

Q: How would you create a RESTful API endpoint in Flask that returns JSON data?
ans:-  You can create a RESTful API endpoint in Flask that returns JSON data by following these steps:
1. **Install Flask-RESTful:** Install Flask-RESTful using `pip install Flask-RESTful`.
2. **Define your API resources:**  Create a class to represent your API resource.  Each resource should have methods for handling different HTTP requests (GET, POST, PUT, DELETE).
3. **Create your API app:** Create an instance of `Api` and add your resource classes to it.
4. **Define your routes:** Use the `add_resource()` method to associate your resource classes with specific URLs.
5. **Return JSON data:**  In the resource methods, use `jsonify()` to convert Python data structures into JSON format.

Here's an example:
```python
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Todo(Resource):
    def get(self, todo_id):
        # Retrieve todo item based on id
        todo = {"id": todo_id, "task": "Learn Flask-RESTful"}
        return jsonify(todo)

api.add_resource(Todo, "/todos/<int:todo_id>")

if __name__ == '__main__':
    app.run(debug=True)
```
This code defines a resource class `Todo` that handles GET requests to `"/todos/<int:todo_id>"`. The `get` method retrieves the todo item based on the given id and returns it as a JSON object.

Q: Explain how to use Flask-WTF to create and validate forms in a Flask application.
ans:-  You can use Flask-WTF to create and validate forms in a Flask application by following these steps:
1. **Install Flask-WTF:** Install Flask-WTF using `pip install Flask-WTF`.
2. **Create a form class:** Create a class that inherits from `FlaskForm` and define the form fields using the appropriate field types.
3. **Use the form in a route:**  Instantiate the form class in your route and use the `form.validate_on_submit()` method to check for form submission and validation.
4. **Handle validation errors:** If the form fails validation, you can access the errors in the `form.errors` dictionary. You can then display these errors to the user in the appropriate way.

Here's an example:
```python
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Handle login logic here
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)
```
This code defines a form class `LoginForm` with two fields, `username` and `password`, both validated using `DataRequired`.  The `login` route handles both GET and POST requests. On POST, it checks the form submission and validation. If successful, it redirects to the `index` route; otherwise, it renders the `login.html` template with the form and potential error messages.

Q: How can you implement file uploads in a Flask application?
ans:-  You can implement file uploads in a Flask application by following these steps:
1. **Configure the `MAX_CONTENT_LENGTH`:**  Set the maximum file size allowed by your application by configuring the `MAX_CONTENT_LENGTH` variable in your Flask app's configuration. This prevents large uploads from crashing your application.
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB
```
2. **Use a form with a file field:**  Use a form with a file field (e.g., `FileField`) to enable users to select files for upload.
3. **Handle the file upload:** In the route that handles the form submission, access the uploaded file using `request.files`.
4. **Save the file:**  Save the uploaded file to your server's storage. You can use the `save()` method of the uploaded file object to save it.
5. **Process the file:** If necessary, you can then process the uploaded file (e.g., resize an image, convert a document to text).
```python
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads' # Set the directory where files will be saved
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

class UploadForm(FlaskForm):
    file = FileField('Upload a file')
    submit = SubmitField('Upload')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload'))
    return render_template('upload.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
```
This code defines an upload form with a `FileField` and a `SubmitField`.  The `upload` route handles both GET and POST requests. On POST, it validates the form and saves the uploaded file to the specified directory if it is valid. It then redirects back to the `upload` route.

Q: Describe the steps to create a Flask blueprint and why you might use one.
ans:-  You can create a Flask blueprint by following these steps:
1. **Create a blueprint object:** Create a new instance of `Blueprint` by passing the name of the blueprint and its URL prefix.
2. **Define routes and views:**  Add your routes and associated view functions to the blueprint object using the `route` decorator.
3. **Register the blueprint:** Register the blueprint with your Flask app using the `register_blueprint` method.
```python
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login')
def login():
    return 'Login page'

@auth.route('/register')
def register():
    return 'Registration page'

app = Flask(__name__)
app.register_blueprint(auth)
```
This code defines a blueprint `auth` with a URL prefix of `/auth`. Two routes, `/login` and `/register`, are added to the blueprint. Finally, the blueprint is registered with the Flask app.

You might use blueprints for several reasons:
1. **Organization:** Structure your application by grouping related functionality into separate blueprints. This makes your code easier to manage and maintain.
2. **Modularity:** Make your code reusable by creating blueprints that can be easily incorporated into different Flask applications.
3. **Namespaces:** Avoid naming conflicts by using blueprints to create namespaces for your routes and view functions.
4. **Testing:** Simplify testing by creating separate test cases for each blueprint.

Q: How would you deploy a Flask application to a production server using Gunicorn and Nginx?
ans:-  You can deploy a Flask application to a production server using Gunicorn and Nginx by following these steps:
1. **Install Gunicorn and Nginx:** Install Gunicorn and Nginx on your server.
2. **Create a Gunicorn configuration file:** Create a configuration file (e.g., `gunicorn.conf.py`) to configure Gunicorn. This file should specify the Flask application to run, the number of worker processes, and other settings.
```python
# gunicorn.conf.py
bind = '0.0.0.0:8000'
workers = 3
worker_class = 'uvicorn.workers.UvicornWorker'
```
3. **Create an Nginx configuration file:** Create a configuration file (e.g., `nginx.conf`) to configure Nginx. This file should define the virtual host for your application, specifying the port to listen on, the location of your static files, and the Gunicorn server to proxy requests to.
```nginx
# nginx.conf
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
4. **Start Gunicorn:** Start Gunicorn using the command `gunicorn -c gunicorn.conf.py your_app:app`. This will start the Gunicorn server, listening on the specified port.
5. **Start Nginx:** Start Nginx using the command `nginx -c nginx.conf`. This will start the Nginx server, listening on port 80 and proxying requests to the Gunicorn server.
6. **Test the deployment:** Access your application in a web browser using your domain name.

Q: Make a fully functional web application using flask, Mangodb. Signup,Signin page.And after successfully login.Say hello Geeks message at webpage.
ans:-  ```python
from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/your_database"
app.config['SECRET_KEY'] = "your_secret_key"
mongo = PyMongo(app)

@app.route("/")
def index():
    if "user" in session:
        return "Hello Geeks!"
    else:
        return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if username already exists
        user = mongo.db.users.find_one({"username": username})
        if user:
            return "Username already exists!"

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the user into the database
        mongo.db.users.insert_one({"username": username, "password": hashed_password})
        return "Registration successful!"

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Find the user in the database
        user = mongo.db.users.find_one({"username": username})
        if user:
            # Check the password
            if check_password_hash(user["password"], password):
                session["user"] = username
                return redirect(url_for("index"))
            else:
                return "Invalid password!"
        else:
            return "Invalid username!"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
```
This code defines a Flask application that uses MongoDB to store user data. The app has three routes: `/`, `/signup`, and `/login`.  
- The `/` route checks if the user is logged in. If so, it displays the "Hello Geeks!" message. Otherwise, it redirects to the `/login` route.
- The `/signup` route handles user registration. It checks if the username is already taken, hashes the password, and inserts the user into the database.
- The `/login` route handles user login. It finds the user in the database, checks the password, and sets a session variable if the login is successful.
- The `/logout` route logs the user out by removing their session data.

**Templates (signup.html, login.html):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
</head>
<body>
    <h1>Signup</h1>
    <form method="POST" action="/signup">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Signup</button>
    </form>
</body>
</html>
```
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>
```


Q: Create a database name Travel_Planner in mysql, and create a table name bookings in that which having attributes (user_id INT, flight_id INT, hotel_id INT, activity_id INT,booking_date DATE).fill with some dummy value.Now you have to read the content of this table using pandas as dataframe.Show the output.
ans:- 
```python
import pandas as pd
import mysql.connector

# Database connection details
mydb = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="Travel_Planner"
)

# Create the cursor object
cursor = mydb.cursor()

# Create the table
cursor.execute("""
    CREATE TABLE bookings (
        user_id INT,
        flight_id INT,
        hotel_id INT,
        activity_id INT,
        booking_date DATE
    )
""")

# Insert dummy data
dummy_data = [
    (1, 101, 201, 301, '2023-08-15'),
    (2, 102, 202, 302, '2023-08-20'),
    (3, 103, 203, 303, '2023-08-25'),
    (4, 104, 204, 304, '2023-09-01'),
    (5, 105, 205, 305, '2023-09-05')
]
cursor.executemany("INSERT INTO bookings VALUES (%s, %s, %s, %s, %s)", dummy_data)
mydb.commit()

# Read data into a pandas DataFrame
query = "SELECT * FROM bookings"
cursor.execute(query)
data = cursor.fetchall()

df = pd.DataFrame(data, columns=["user_id", "flight_id", "hotel_id", "activity_id", "booking_date"])

print(df)

# Close the cursor and connection
cursor.close()
mydb.close()
```
This code first establishes a connection to your MySQL database. Then, it creates the `bookings` table with the specified attributes and inserts some dummy data. Finally, it uses `pd.DataFrame` to read the data from the table into a DataFrame and prints the output.




Q1.3. name = ["Mohan", "dash", "karam", "chandra", "gandhi", "Bapu"]
do the following operations in this list;
a) add an element "freedom_fighter" in this list at the 0th index.
ans:- name.insert(0,"freedom_fighter")
b) find the output of the following ,and explain how?
name = ["freedomFighter", "Bapuji", "Mohan", "dash", "karam", "chandra", "gandhi"]
length1=len(name)-len(name)+1:1:2])
length2=len(name)-len(name)+1:-1:1])
print(length1+length2)
ans:-  The output will be 7. The length of the list is 7, and both length1 and length2 are calculating the length of the list. So, length1 + length2 = 7 + 0 = 7.
c) add two more elements in the name ["Netaji","Bose"] at the end of the list.
ans:-  name.extend(["Netaji","Bose"])
d) what will be the value of temp:
name = ["Bapuji", "dash", "karam", "chandra", "gandhi", "Mohan"]
temp=name[-1]
name[-1]=name[0]
name[0]=temp
print(name)
ans:- ["Mohan", "dash", "karam", "chandra", "gandhi", "Bapuji"]
Q1.4.Find the output of the following.
animal = ["Human","cat","mat","cat","rat","Human","Lion"]
print(animal.count('Human'))
print(animal.index('rat'))
print(len(animal))
ans:-
2
4
7Q: Write a program for VIBGYOR Spectrum based on their Wavelength using. Wavelength Range:
ans:- 
```python
colors = {
    "Violet": "400.0-440.0",
    "Indigo": "440.0-460.0",
    "Blue": "460.0-500.0",
    "Green": "500.0-570.0",
    "Yellow": "570.0-590.0",
    "Orange": "590.0-620.0",
    "Red": "620.0-720.0",
}

for color, wavelength in colors.items():
    print(f"{color} - {wavelength}")

```

Q: Consider the gravitational interactions between the Earth, Moon, and Sun in our solar system. Given:
mass_earth = 5.972e24 # Mass of Earth in kilograms
mass_moon = 7.34767309e22 # Mass of Moon in kilograms
mass_sun = 1.989e30 # Mass of Sun in kilograms
distance_earth_sun = 1.496e11 # Average distance between Earth and Sun in meters
distance_moon_earth = 3.844e8 # Average distance between Moon and Earth in meters
Tasks:
* Calculate the gravitational force between the Earth and the Sun.
* Calculate the gravitational force between the Moon and the Earth.
* Compare the calculated forces to determine which gravitational force is stronger.
* Explain which celestial body (Earth or Moon) is more attracted to the other based on the comparison.
ans:- 
```python
import math

# Constants
G = 6.67430e-11 # Gravitational constant

# Given values
mass_earth = 5.972e24 # kg
mass_moon = 7.34767309e22 # kg
mass_sun = 1.989e30 # kg
distance_earth_sun = 1.496e11 # m
distance_moon_earth = 3.844e8 # m

# Calculate gravitational force between Earth and Sun
force_earth_sun = (G * mass_earth * mass_sun) / (distance_earth_sun**2)

# Calculate gravitational force between Moon and Earth
force_moon_earth = (G * mass_moon * mass_earth) / (distance_moon_earth**2)

# Compare the forces
print(f"Gravitational force between Earth and Sun: {force_earth_sun:.2e} N")
print(f"Gravitational force between Moon and Earth: {force_moon_earth:.2e} N")

# Determine which force is stronger
if force_earth_sun > force_moon_earth:
    print("The gravitational force between Earth and Sun is stronger.")
else:
    print("The gravitational force between Moon and Earth is stronger.")

# Explain the attraction
print("The Earth is more attracted to the Sun because the gravitational force between them is much stronger due to the larger mass of the Sun and the greater distance between Earth and the Sun compared to the Moon and Earth.")
```Q: Question 1.5. tuple1=(10,20,"Apple",3.4,'a',["master","j"],("sita","geeta",22),[{"roll_no":13},{"name":"Navneet"}] )
ans:- a) print(len(tuple1))
ans:- b) print(tuple1[ -1][ -1]["name"])
ans:- c) fetch the value of roll_no from this tuple.
ans:- d) print(tuple1[ -3][1])
ans:- e) fetch the element "22" from this tuple.
Q: 1.6. Write a program to display the appropriate message as per the color of signal(RED-Stop/Yellow-Stay/Green-Go) at the road crossing.
ans:- 
Q: 1.7. Write a program to create a simple calculator performing only four basic operations(+,-,*,/).
ans:- 
Q: 1.8. Write a program to find the larger of the three pre-specified numbers using ternary operators.
ans:- 
Q: 1.9. Write a program to find the factors of a whole number using a while loop.
ans:- 
Q: 1.10. Write a program to find the sum of all the positive numbers entered by the user. As soon as the user enters a negative number, stop taking in any further input from the user and display the sum.
ans:- 
Q: 1.11. Write a program to find prime numbers between 2 to 100 using nested for loops.
ans:- 
Q: 1.12. Write the programs for the following:
- Accept the marks of the student in five major subjects and display the same.
- Calculate the sum of the marks of all subjects.Divide the total marks by number of subjects (i.e. 5), calculate percentage = total marks/5 and display the percentage.
- Find the grade of the student as per the following criteria. Hint: Use Match & case for this:

| Criteria | Grade |
|---|---|
| percentage > 85 | A |
| percentage < 85 && percentage >= 75 | B |
| percentage < 75 && percentage >= 50 | C |
| percentage > 30 && percentage <= 50 | D |
| percentage < 30 | Reappear |
ans:- 
Q: Define a Python module named constants.py containing constants like pi and the speed of light.
ans:-  ```python
# constants.py
pi = 3.14159
speed_of_light = 299792458
```

Q: Write a Python module named calculator.py containing functions for addition, subtraction, multiplication, and division.
ans:-  ```python
# calculator.py
def add(x, y):
  """Returns the sum of two numbers."""
  return x + y

def subtract(x, y):
  """Returns the difference of two numbers."""
  return x - y

def multiply(x, y):
  """Returns the product of two numbers."""
  return x * y

def divide(x, y):
  """Returns the quotient of two numbers."""
  if y == 0:
    return "Division by zero error!"
  else:
    return x / y
```

Q: Implement a Python package structure for a project named ecommerce, containing modules for product management and order processing.
ans:- 
```
ecommerce/
├── __init__.py
├── product_management/
│   ├── __init__.py
│   ├── product.py
│   ├── category.py
│   └── inventory.py
├── order_processing/
│   ├── __init__.py
│   ├── order.py
│   ├── payment.py
│   └── shipping.py
└── utils/
    ├── __init__.py
    ├── database.py
    └── logger.py
```
* **ecommerce/__init__.py:** This file is the entry point for the package and can be used to define global variables or functions used throughout the package.
* **product_management/__init__.py:** This file acts as a placeholder to indicate that this directory is a Python package.
* **product_management/product.py:** This module defines the Product class and its attributes and methods for managing product data.
* **product_management/category.py:** This module defines the Category class and its attributes and methods for managing product categories.
* **product_management/inventory.py:** This module manages the inventory of products.
* **order_processing/__init__.py:**  This file acts as a placeholder to indicate that this directory is a Python package.
* **order_processing/order.py:** This module defines the Order class and its attributes and methods for managing orders.
* **order_processing/payment.py:** This module handles payment processing for orders.
* **order_processing/shipping.py:** This module handles shipping details for orders.
* **utils/__init__.py:**  This file acts as a placeholder to indicate that this directory is a Python package.
* **utils/database.py:** This module provides functions for interacting with a database (e.g., connecting, querying, updating).
* **utils/logger.py:** This module provides functions for logging events and debugging information.

Q: Implement a Python module named string_utils.py containing functions for string manipulation, such as reversing and capitalizing strings.
ans:- ```python
# string_utils.py
def reverse_string(text):
  """Reverses a given string."""
  return text[::-1]

def capitalize_string(text):
  """Capitalizes the first letter of each word in a string."""
  return text.title()
```

Q: Write a Python module named file_operations.py with functions for reading, writing, and appending data to a file.
ans:- ```python
# file_operations.py
def read_file(file_path):
  """Reads the contents of a file."""
  with open(file_path, "r") as file:
    data = file.read()
  return data

def write_file(file_path, data):
  """Writes data to a file."""
  with open(file_path, "w") as file:
    file.write(data)

def append_file(file_path, data):
  """Appends data to a file."""
  with open(file_path, "a") as file:
    file.write(data)
```

Q: Write a Python program to create a text file named "employees.txt" and write the details of employees, including their name, age, and salary, into the file.
ans:- ```python
# employee_details.py
def create_employee_file():
  """Creates a text file named 'employees.txt' and writes employee details."""
  file_path = "employees.txt"
  with open(file_path, "w") as file:
    file.write("Name,Age,Salary\n")
    while True:
      name = input("Enter employee name (or 'exit' to quit): ")
      if name.lower() == "exit":
        break
      age = input("Enter employee age: ")
      salary = input("Enter employee salary: ")
      file.write(f"{name},{age},{salary}\n")

if __name__ == "__main__":
  create_employee_file()
```

Q: Develop a Python script that opens an existing text file named "inventory.txt" in read mode and displays the contents of the file line by line.
ans:- ```python
# inventory_reader.py
def read_inventory_file():
  """Reads the contents of 'inventory.txt' line by line."""
  file_path = "inventory.txt"
  with open(file_path, "r") as file:
    for line in file:
      print(line.strip())

if __name__ == "__main__":
  read_inventory_file()
```

Q: Create a Python script that reads a text file named "expenses.txt" and calculates the total amount spent on various expenses listed in the file.
ans:- ```python
# expenses_calculator.py
def calculate_total_expenses():
  """Calculates the total expenses from 'expenses.txt'."""
  file_path = "expenses.txt"
  total_expenses = 0
  with open(file_path, "r") as file:
    for line in file:
      expense = float(line.strip())
      total_expenses += expense
  print(f"Total expenses: {total_expenses}")

if __name__ == "__main__":
  calculate_total_expenses()
```

Q: Create a Python program that reads a text file named "paragraph.txt" and counts the occurrences of each word in the paragraph, displaying the results in alphabetical order.
ans:- ```python
# paragraph_word_count.py
import collections

def count_words_in_paragraph():
  """Counts word occurrences in 'paragraph.txt' and displays alphabetically."""
  file_path = "paragraph.txt"
  word_counts = collections.Counter()
  with open(file_path, "r") as file:
    for line in file:
      words = line.lower().split()
      word_counts.update(words)

  sorted_word_counts = dict(sorted(word_counts.items()))
  for word, count in sorted_word_counts.items():
    print(f"{word}: {count}")

if __name__ == "__main__":
  count_words_in_paragraph()
```

