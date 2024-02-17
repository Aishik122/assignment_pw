from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'D:\PW_Data_science\Python\Flask_assignment1/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # List all files in the uploads folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

## index . html 
    '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload App</title>
</head>
<body>
    <h1>Uploaded Files</h1>
    <ul>
        {% for file in files %}
            <li>{{ file }}</li>
        {% endfor %}
    </ul>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".txt, .pdf, .png, .jpg, .jpeg, .gif">
        <input type="submit" value="Upload">
    </form>
</body>
</html>'''
