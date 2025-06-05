from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # if username == "harshit" and password == "hiibuddy":
    #     return render_template("home.html", name = username)

    valid_users = {
        "Harshit" : "123",
        "deepa" : "456",
        "kunal" : "789"
    }

    if username in valid_users and password == valid_users[username]:
        return render_template("home.html", name=username)
    
    return render_template("login.html")

