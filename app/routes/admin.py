from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from app import db
from app.models import parking_lot, parking_spot, reservation, client
from functools import wraps 
# wraps used for decorator in user authentication
from sqlalchemy import or_, cast, String

admin_bp = Blueprint('admin', __name__)

# code to check authentication
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('auth.adminlogin'))
        return f(*args, **kwargs)
    return decorated_function
    

# code to view all available parking lots locations
@admin_bp.route('/home')
@admin_required
def view_lots():

    lots = parking_lot.query.filter_by(status='active').all()
    old_lots = parking_lot.query.filter_by(status='deleted').all()
    return render_template('admin/admin_dash.html', lots=lots, old_lots=old_lots)

@admin_bp.route('/reopen_lot/<int:lot_id>')
@admin_required
def reopen_lot(lot_id):
    
    data = parking_lot.query.get(lot_id)
    if data:
        if data.status == 'deleted':
            data.status = 'active'
            for spot in data.spots:
                spot.is_active = True
            db.session.commit()
        else:
            flash('Parking Lot already present', 'warning')
            return redirect(url_for('admin.view_lots'))
    
    return redirect(url_for('admin.view_lots'))


# code to add new parking location
@admin_bp.route('/create-lot', methods=["GET", "POST"])
@admin_required
def create_lot():
    
    if request.method == "POST":
        location = request.form.get('location') # location is the name of parking lot
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        totalspots = request.form.get('totalspots')
        price = request.form.get('price')

        existing = parking_lot.query.filter_by(location=location, status='active').first()
    
        if not existing:
            new_lot = parking_lot( location=location, address=address, pin_code=pincode, total_spots=totalspots, price=price)

            db.session.add(new_lot)
            db.session.commit()

            for _ in range(int(totalspots)):
                new_spot = parking_spot(lot_id=new_lot.lot_id, status='available')
                db.session.add(new_spot)

            db.session.commit()
            flash('New parking lot added successfully', 'success')

            return redirect(url_for('admin.view_lots'))
        
        else: 
            flash("Location already exists!", "danger")
            return redirect(url_for('admin.create_lot'))
    
    return render_template('admin/forms/lot_form.html')


# Update lot details
@admin_bp.route('/update-lot/<int:lot_id>', methods=["GET", "POST"])
@admin_required
def update_lot(lot_id):

    data = parking_lot.query.filter_by(lot_id=lot_id).first()

    if not data:
        flash("Lot not found.", "danger")
        return redirect(url_for('admin.view_lots'))

    if request.method == "POST":
        # Only editable fields are updated
        data.location = request.form.get('location')
        data.price = request.form.get('price')

        db.session.commit()
        flash("Lot updated successfully", "success")

        return redirect(url_for('admin.view_lots'))

    # If from GET method, render form with existing values
    return render_template( 'admin/forms/lot_form.html', lot_id=data.lot_id, location=data.location, address=data.address, pincode=data.pin_code, totalspots=data.total_spots, price=data.price)



# delete parking lot if completly empty
@admin_bp.route('/delete-lot/<int:lot_id>')
@admin_required
def delete_lot(lot_id):

    lot = parking_lot.query.get(lot_id)
    if not lot:
        return "Lot not found", 404

    for spot in lot.spots:
        if spot.status != 'available':
            flash("Cannot delete: Some spots are occupied.", "warning")
            return redirect(url_for('admin.view_lots'))
    else:
        for spot in lot.spots:
            spot.is_active = False

    lot.status = 'deleted'
    db.session.commit()
    flash('Parking lot has been successfully deleted.', 'success')
    return redirect(url_for('admin.view_lots'))



# view parking spot
@admin_bp.route('/view-spot/<int:spot_id>')
@admin_required
def view_spot(spot_id):
    data = parking_spot.query.get(spot_id)

    if not data:
        return redirect(url_for('admin.view_lots'))

    reservation_id = None
    if data.status == 'occupied':
        res = reservation.query.filter_by(spot_id=spot_id, status='active').first()
        if res:
            reservation_id = res.reservation_id

    return render_template( 'admin/forms/view_spot.html', spot_id=data.spot_id, status=data.status, reservation_id=reservation_id )



# delete parking spot if empty
@admin_bp.route('/delete-spot/<int:spot_id>')
@admin_required
def delete_spot(spot_id):
    
    spot = parking_spot.query.get(spot_id)
    if not spot:
        return "Lot not found", 404

    if spot.status == 'occupied':
        flash("Can't delete an occupied spot", 'danger')
        return redirect(url_for('admin.view_spot', spot_id=spot_id))
        
    spot.is_active = False
    db.session.commit()
    flash('Spot deleted successfully', 'success')
    return redirect(url_for('admin.view_lots'))



@admin_bp.route('/view-occupied-spot/<int:reservation_id>')
@admin_required
def view_occupied_spot(reservation_id):
    return redirect(url_for('admin.occupied_spot', reservation_id=reservation_id))


# view occupied parking spot details
@admin_bp.route('/occupied-spot/<int:reservation_id>')
@admin_required
def occupied_spot(reservation_id):

    data = reservation.query.get(reservation_id)

    if data:
        return render_template('admin/forms/occupied_spot.html', reservation_id=data.reservation_id, email=data.user_email, vehicle=data.vehicle_no, time=data.parking_time, spot_id=data.spot_id, price=data.lot.price)
        # stot_id is needed for Close button to get back to view_spot from child table which is revervation
    flash("Reservation not found", "danger")
    return redirect(url_for('admin.view_spot', spot_id = data.spot_id))



# view all users
@admin_bp.route('/view-users', methods=["POST", "GET"])
@admin_required
def view_users():

    if request.method == "POST":
        data = request.form.get('search_for')

        if data:
            search_for = f"%{data}%"
            users = client.query.filter(
                or_(
                        client.name.ilike(search_for),
                        client.email.ilike(search_for),
                        client.address.ilike(search_for),
                        cast(client.pincode, String).ilike(search_for)
                )
            ).all()
        else:
            flash("Please enter a keyword to search.", "warning")
            users = client.query.all()
            return render_template('admin/view_users.html', users=users)
        
    else:
        users = client.query.all()
    return render_template('admin/view_users.html', users=users)



# temprary summary dashboard
@admin_bp.route('/dashboard')
@admin_required
def dashboard_summary():
    total_lots = parking_lot.query.filter_by(status='active').count()
    total_spots = parking_spot.query.count()
    occupied = parking_spot.query.filter_by(status='occupied').count()
    users = client.query.count()

    return render_template("admin/dashboard.html", lots=total_lots, spots=total_spots, occupied=occupied, users=users)
