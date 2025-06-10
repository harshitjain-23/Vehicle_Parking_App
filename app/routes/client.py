from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from app import db
from app.models import parking_lot, parking_spot, reservation, client
from functools import wraps 

client_bp = Blueprint('client', __name__)

# code to check authentication
def user_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# client dashboard
@client_bp.route('/')
@user_authentication
def dashboard():
    return render_template('client/dashboard.html')


@client_bp.route('/user-profile')
@user_authentication
def profile(email):
    return render_template(url_for(''))
# need to check for each user details seperatly 