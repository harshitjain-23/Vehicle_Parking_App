from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from app import db
from app.models import parking_lot, parking_spot, reservation, client
from functools import wraps 
from sqlalchemy import or_
from sqlalchemy.sql import cast
from sqlalchemy.types import String
from datetime import datetime
import math


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
    return render_template('templates/client/dashboard.html')


@client_bp.route('/user-profile')
@user_authentication
def profile():
    email = session.get('user')
    data = client.query.get(email)
    return render_template('client/profile.html', user=data)


@client_bp.route('/update-profile', methods=['POST', 'GET'])
@user_authentication
def update_profile():
    email = session.get('user')

    if not email:
        flash("user not found.", "danger")
        return redirect(url_for('client.dashboard'))

    data = client.query.get(email)

    if request.method == 'POST':
        data.name = request.form.get('name')
        data.address = request.form.get('address')
        data.pincode = request.form.get('pincode')
        data.password =request.form.get('password')

        db.session.commit()
        flash('Profile successfully updated', 'success')
        return redirect(url_for('client.profile'))
    
    return render_template('client/update_profile.html', user)


@client_bp.route('/locations', methods=['POST', 'GET'])
@user_authentication
def locations():
    filters = [parking_lot.status == 'active']  # Base filter

    if request.method == "POST":
        search = request.form.get('search_for', '').strip()

        if search:
            search_pattern = f"%{search}%"
            filters.append(
                or_(
                    parking_lot.location.ilike(search_pattern),
                    cast(parking_lot.pin_code, String).ilike(search_pattern)
                )
            )
        else:
            flash("Please enter a keyword to search.", "warning")

    data = parking_lot.query.filter(*filters).all()
    return render_template('client/locations.html', data=data)




@client_bp.route('/booking/<int:lot_id>', methods=["POST", "GET"])
@user_authentication
def booking(lot_id):

    # false status means not occupies and is_active means spot is not deleted 
    vacant_spot = parking_spot.query.filter_by(lot_id=lot_id, status='available', is_active=True).first()
    user_email = session.get('user')
    lot = parking_lot.query.get(lot_id)

    if not vacant_spot:
        flash("No available spots in this parking lot.", "warning")
        return redirect(url_for('client.locations'))
    
    if request.method == 'POST':
        vehicle_no = request.form.get('vehicle_no')
        existing = reservation.query.filter_by(vehicle_no = vehicle_no, status='active').all()

        if existing:
            flash("Same vehicle can't be parked at more than one spot at the time", 'warning')
            return render_template('client/booking.html', lot_id = lot_id, user_email=user_email, spot_id=vacant_spot.spot_id)
        
        else:
            reserve = reservation(lot_id=lot_id, vehicle_no=vehicle_no, spot_id=vacant_spot.spot_id, user_email=user_email)
            vacant_spot.status = 'occupied'

            db.session.add(reserve)
            db.session.commit()

            flash("Spot successfully booked!", "success")
            return redirect(url_for('client.reservations'))
            
    return render_template('client/booking.html', user_email=user_email, spot_id=vacant_spot, lot_id=lot.lot_id,location=lot.location, address=lot.address, pincode=lot.pincode, price=lot.price )




@client_bp.route('/reservation')
@user_authentication
def reservations():
    user_email = session.get('user')
    new_reservations = reservation.query.filter_by(status='active', user_email=user_email).all()
    old_reservations = reservation.query.filter_by(status='deleted', user_email=user_email).all()
    return render_template('client/reservations.html', new=new_reservations, old=old_reservations)


@client_bp.route('/release/<int:reservation_id>', methods=['POST', 'GET'])
@user_authentication
def release(reservation_id):
    reserve = reservation.query.get_or_404(reservation_id)

    if reserve.status != 'active':
        flash("Reservation already released.", "warning")
        return redirect(url_for('client.reservations'))

    leave = datetime.now()
    duration = leave - reserve.parking_time
    hours = duration.total_seconds() / 3600
    rounded_hours = math.ceil(hours)
    price_per_hour = reserve.spot.lot.price
    cost = rounded_hours * price_per_hour

    if request.method == 'POST':
        reserve.leaving_time = leave
        reserve.total_cost = cost
        reserve.status = 'deleted'
        reserve.spot.status = 'available'

        db.session.commit()
        flash("Parking slot released successfully.", "success")
        return redirect(url_for('client.reservations'))

    return render_template( 'client/release.html', reservation_id=reservation_id, lot_id=reserve.lot_id, spot_id=reserve.spot_id, vehicle_no=reserve.vehicle_no, parking_time=reserve.parking_time, leaving_time=leave, total_cost=cost )
