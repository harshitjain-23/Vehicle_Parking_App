import sqlite3

# This script creates the database schema for my parking system application using Sqlite3 database


# Connect to database (or create it if it doesn't exist)
conn = sqlite3.connect('parking_system.db')
cursor = conn.cursor()

# Create Admin table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Admin (
    Username TEXT PRIMARY KEY,
    Password TEXT NOT NULL
)
''')

# Insert admin login credentials into database
cursor.execute('''
INSERT INTO Admin (Username, Password)
VALUES ('Admin', 'admin@123#')
''' )


# Create user table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    Email_id TEXT PRIMARY KEY UNIQUE NOT NULL,
    password TEXT NOT NULL CHECK (length(password) >= 8),
    fname TEXT NOT NULL,
    lname TEXT,
    address TEXT NOT NULL,
    pincode INTEGER NOT NULL CHECK (length(pincode) >= 8)
)
''')

# Create parking_lot table
cursor.execute('''
CREATE TABLE IF NOT EXISTS parking_lot (
    lot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prime_location_name TEXT NOT NULL UNIQUE,
    address TEXT COLLATE NOCASE NOT NULL,
    pin_code INTEGER NOT NULL CHECK (pin_code BETWEEN 100000 AND 999999),
    maximum_number_of_spots INTEGER NOT NULL CHECK (maximum_number_of_spots >= 0),
    price INTEGER NOT NULL CHECK (price >= 1)
)
''')

# Create parking_slot table
cursor.execute('''
CREATE TABLE IF NOT EXISTS parking_slot (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lot_id INTEGER,
    status TEXT COLLATE NOCASE CHECK (status IN ('O', 'A', 'O-occupied', 'A-available', 'occupied', 'available')),
    FOREIGN KEY (lot_id) REFERENCES parking_lot (lot_id) ON DELETE CASCADE ON UPDATE CASCADE
)
''')

# Create reserve_parking_spot table
cursor.execute('''
CREATE TABLE IF NOT EXISTS reserve_parking_spot (
    reserved_spot_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    spot_id INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    parking_timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    leaving_timestamp TEXT,
    FOREIGN KEY (spot_id) REFERENCES parking_slot (slot_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user (Email_id) ON DELETE RESTRICT ON UPDATE CASCADE
)
''')

# Save changes and close connection
conn.commit()
conn.close()

print("Database & tables created successfully.")
