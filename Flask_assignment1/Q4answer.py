from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/home", methods=["GET","POST"])
def home():
    if request.method =="POST":
        name = request.form["name"]
        return render_template("index.html", name=name)
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)