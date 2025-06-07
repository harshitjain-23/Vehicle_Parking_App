from flask import Flask, request, render_template, url_for, redirect, flash # type: ignore

app = Flask(__name__)
app.secret_key = "so-secret"

@app.route("/")
def form():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")


        if not user and not password:
            flash("Name and password field can't be empty")
            return redirect(url_for("form"))
        
        elif not user:
            flash("Name field can't be empty")
            return redirect(url_for("form"))
        
        elif not password:
            flash("Password field can't be empty")
            return redirect(url_for("form"))
        
        else:
            flash(f"Thanks {user} for your response")
            return redirect(url_for("thankyou", username=user))

    # if user == "Harshit" and password == "123":
    #     return render_template("thankyou.html")
    
    return render_template("form.html")

@app.route("/thankyou")
def thankyou():
    user = request.args.get("username")
    return render_template("thankyou.html", name=user)

@app.route("/test")
def test():
    flash("This is a test message!")
    return redirect(url_for("thankyou"))

