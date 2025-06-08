from flask import Blueprint, redirect, render_template, request, flash, session, url_for
from app import db
from app.models import parking_lot, parking_spot, reservation, client

admin_bp = Blueprint('admin', __name__)



# code to view all available parking lots locations
@admin_bp.route('/')
def view_lots():

    if 'admin' not in session:
        return redirect(url_for('auth.adminlogin'))
    
    lots = parking_lot.query.all()
    return render_template('admin/view_lots.html', lots=lots)
## need to fetch all spots details with their correspondig lots by running a for loop and then passing lots and spots in a key value pair passes to render_template



# code to add new parking location
@admin_bp.route('/create-lot', methods=["GET", "POST"])
def create_lot():

    if 'admin' not in session:
        return redirect(url_for('auth.adminlogin'))
    
    location = request.form.get('loction') # location is the name of parking lot
    address = request.form.get('address')
    pincode = request.form.get('pincode')
    totalspots = request.form.get('totalspots')
    price = request.form.get('price')

    all_location = parking_lot.query.all()

    if location not in all_location:

        new_lot = parking_lot( location=location, address=address, pin_code=pincode, total_spots=totalspots, price=price)
        
        db.session.add(new_lot)
        db.session.commit()
        flash('New parking lot added successfully', 'success')

        return redirect(url_for('admin.view_lots'))
    
    return redirect(url_for('create_lot.html'))



# code to view single lot details ( pre-view form )
@admin_bp.route('/view-lot/<int:lot_it>')
def view_lot(lot_id):

    if 'admin' not in session:
        return redirect(url_for('auth.adminlogin'))
    
    details = parking_lot.query.get(lot_id)

    if details:
        return render_template('create_lot.html', lot_id=details.lot_id, location=details.location, address=details.address, pincode=details.pin_code, totalspots=details.total_spots, price=details.price)

    return redirect(url_for('view_lot'))



# Update lot details
@admin_bp.route('/update-lot/<int:lot_id>', methods=["POST", "GET"])
def update_lot(lot_id):

    if 'admin' not in session:
        return redirect(url_for('auth.adminlogin'))
    
    data = parking_lot.query.filter_by(lot_id=lot_id).first()

    data.location = request.form.get('location')
    data.price = request.form.get('price') 

    db.session.commit()
    return redirect(url_for('view_lots'))


# delete parking lot if completly empty
# view parking spot
# view occupied parking spot details
# delete parking spot if empty
# view all users
# searching into the database
# summary dashboard
