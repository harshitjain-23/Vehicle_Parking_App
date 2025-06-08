from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from app import db
from app.models import client, superuser

auth_bp = Blueprint('auth', __name__)


# Client / User Login
@auth_bp.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        data = client.query.filter_by(username=username).first()

        if username == data.username and password == data.password:
            session['user'] = username
            flash('Login successfull', 'success')
            return redirect(url_for("client"))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for("login.html"))
        
    return render_template("login.html")    
    

# Admin Login
@auth_bp.route('/admin', methods=["GET","POST"])
def adminlogin():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        data = superuser.query.filter_by(username=username).first()

        if username == data.username and password == data.password:
            session['admin'] = username
            flash('Login successfull', 'success')
            return redirect(url_for("admin"))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for("adminlogin.html"))
        
    return render_template("adminlogin.html") 


# Client logout 
@auth_bp.route('/logout')
def clientlogout():
    session.pop('user', None)
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))


# Admin logout
@auth_bp.route('/logout-admin')
def adminlogout():
    session.pop('admin', None)
    flash('Logged out', 'info')
    return redirect(url_for('auth.adminlogin'))