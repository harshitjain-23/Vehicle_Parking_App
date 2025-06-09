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
        
    return render_template("/login/login.html")    
    

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
        
    return render_template("/login/adminlogin.html") 


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

# signup
@auth_bp.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":

        email = request.form.get('email')
        name = request.form.get('name')
        address= request.form.get('address')
        pincode = request.form.get('pincode')
        password = request.form.get('password')

        existing_user = client.query.filer_by(email=email).first()

        if existing_user:
            flash('User already exits please login.', 'warning')
            return redirect(url_for('auth.login'))

        new_user = client(name=name, email=email, address=address, pincode=pincode, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('/login/signup.html')
        
