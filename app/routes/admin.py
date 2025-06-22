from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from app import db
from app.models import parking_lot, parking_spot, reservation, client
from functools import wraps 
# wraps used for decorator in user authentication
from sqlalchemy import or_, cast, String
import io
import base64
import matplotlib.pyplot as plt
from sqlalchemy.sql import func


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



# Admin Search Page
@admin_bp.route('/search', methods=['GET'])
@admin_required
def search():
    query = request.args.get('query', '').strip()
    category = request.args.get('category', '').strip()
    results = []
    columns = []

    if query and category:
        if category == 'lot':
            lots = parking_lot.query.filter(
                (parking_lot.location.ilike(f'%{query}%')) |
                (parking_lot.address.ilike(f'%{query}%')) |
                (parking_lot.pin_code.ilike(f'%{query}%')) |
                (parking_lot.status.ilike(f'%{query}%'))
            ).all()
            columns = ['ID', 'Location', 'Address', 'Pincode', 'Status']
            results = [
                [lot.lot_id, lot.location, lot.address, lot.pin_code, lot.status]
                for lot in lots
            ]

        elif category == 'client':
            clients = client.query.filter(
                (client.name.ilike(f'%{query}%')) |
                (client.email.ilike(f'%{query}%')) |
                (client.address.ilike(f'%{query}%')) |
                (client.pincode.ilike(f'%{query}%'))
            ).all()
            columns = ['Name', 'Email', 'Address', 'Pincode']
            results = [
                [c.name, c.email, c.address, c.pincode]
                for c in clients
            ]

        elif category == 'reservation':
            reservations = reservation.query.filter(
                (reservation.vehicle_no.ilike(f'%{query}%')) |
                (reservation.user_email.ilike(f'%{query}%')) |
                (reservation.status.ilike(f'%{query}%'))
            ).all()
            columns = ['ID', 'User Email', 'Vehicle No', 'Parking Time', 'Leaving Time', 'Status']
            results = [
                [r.reservation_id, r.user_email, r.vehicle_no, r.parking_time, r.leaving_time or '—', r.status]
                for r in reservations
            ]

        elif category == 'spot':
            spots = parking_spot.query.filter(
                (parking_spot.status.ilike(f'%{query}%')) |
                (parking_spot.spot_id.cast(db.String).ilike(f'%{query}%')) |
                (parking_spot.lot_id.cast(db.String).ilike(f'%{query}%'))
            ).all()
            columns = ['Spot ID', 'Lot ID', 'Status', 'Active']
            results = [
                [s.spot_id, s.lot_id, s.status, 'Yes' if s.is_active else 'No']
                for s in spots
            ]

    return render_template('admin/search.html', results=results, columns=columns, query=query, category=category)



@admin_bp.route('/admin-summary')
@admin_required
def admin_summary():
    total_lots = parking_lot.query.filter_by(status='active').count()
    total_spots = parking_spot.query.filter_by(is_active=True).count()
    avg_price = db.session.query(func.avg(parking_lot.price)).scalar() or 0
    total_clients = client.query.count()

    avg_spots_per_lot = total_spots // total_lots if total_lots else 0
    total_reservations = reservation.query.count()
    current_active_reservations = reservation.query.filter_by(status='active').count()

    total_revenue = db.session.query(func.sum(reservation.total_cost)).scalar() or 0

    avg_revenue_per_client = total_revenue / total_clients if total_clients else 0

    completed_reservations = reservation.query.filter(reservation.leaving_time != None).all()
    total_duration = 0
    for r in completed_reservations:
        duration = (r.leaving_time - r.parking_time).total_seconds() / 3600
        total_duration += duration
    avg_parking_duration = total_duration / len(completed_reservations) if completed_reservations else 0


    return render_template('admin/summary.html',
        total_lots=total_lots,
        total_spots=total_spots,
        avg_price=round(avg_price, 2),
        avg_spots_per_lot= avg_spots_per_lot,
        total_revenue=round(total_revenue, 2),
        current_active=current_active_reservations,
        total_reservations=total_reservations,
        total_clients=total_clients,
        avg_duration=round(avg_parking_duration, 2),
        avg_revenue=round(avg_revenue_per_client, 2),
    )
