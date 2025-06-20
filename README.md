# 🚗 Vehicle Parking Management System

A full-stack web-based Parking Management System designed to streamline the parking process for users and administrators. This system allows users to book and release parking spots, while admins can manage lots, monitor usage, and analyze statistics with a clean UI, efficient workflows, and smart automation. Built using **Flask**, **SQLite**, and **Bootstrap**, it includes separate dashboards for **Admins** and **Clients**

---

## 👨‍💻 Author

**Name:** Harshit Jain  
**Email:** jainharshit2305@gmail.com <br>
**LinkedIn**: linkedin.com/in/harshit2305

---

## 📝 Description

This project simulates a real-time vehicle parking platform that allows:
- Clients to register, log in, book and release parking slots.
- Admins to manage parking lots and users, and monitor system performance using analytical summaries.

---

## 🛠 Tech Stack

| Layer           | Technology                  |
|-----------------|------------------------------
| Backend         | Python, Flask, SQLAlchemy   |
| Frontend        | HTML, CSS, Bootstrap 5      |
| Database        | SQLite                      |
| Template Engine | Jinja2                      |
| Session/Auth    | Flask Sessions              |

---

## 🛠️ Features

### 🔐 Authentication
- Secure login/signup for **Clients**
- Separate **Admin** login

### 🛡️ Admin
- Create/Update/Delete Parking Lots (only if empty)
- Auto-generate parking spots
- View graphical representation of lot status (🟢 A / 🔴 O style)
- View all users, lots, spots, and reservations
- Search by category (client, lot, spot, reservation)
- View full admin summary dashboard with charts

### 👥 Client
- Personalized greeting and profile update
- View and book available parking spots
- Auto-allocation of the first available spot
- View current and past reservations
- Release spot & see cost based on time
- View history and analytics summary

---

## 🖼 UI Highlights

- 🎨 Minimalist and elegant UI using Bootstrap 5
- 🧩 Graphical Lot View with intuitive colors
- 📱 Mobile Responsive Layout
- 🧾 Table-based listings for reservations, users, and lots
- ✍️ Auto-filled forms using session data

---

## 🗂️ Project Structure

Vehicle_Parking_App/ <br>
│ <br>
├── app/<br>
│ ├── models/ <br>
│ ├── routes/ <br>
│ ├── templates/ <br>
│ ├── static/ <br>
│ └── init.py <br>
│ <br>
├── run.py <br>
└── README.md <br>


---

## 🧠 Database Schema Overview

### `client`
- email (PK), name, address, pincode, password

### `parking_lot`
- lot_id (PK), location, address, pin_code, price, status

### `parking_spot`
- spot_id (PK), lot_id (FK), status, is_active

### `reservation`
- reservation_id (PK), lot_id (FK), spot_id (FK), user_email (FK)
- vehicle_no, parking_time, leaving_time, total_cost, status

---


## 📊 Summary Dashboards

- **Admin Summary**: All system-wide statistics
- **User Summary**: Personalized booking analytics

---

## 📎 How to Run the App

```bash

### Step 1:  Clone the Repository
git clone https://github.com/23f3001028/Vehicle_Parking_App/ <br>
cd vehicle-parking-system

### Step 2: Create a Virtual Environment (optional but recommended)
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate


# Step 3: Install dependencies
pip install -r requirements.txt

# Step 2: Run the server
python run.py

# Step 3: Open in browser
http://127.0.0.1:5000

```

## ❤️ Acknowledgements
Made with passion, purpose, and plenty of Python. <br>
This project reflects the challenges of real-world parking systems and aims to simplify them for users and admins alike.

---

## 🌟 Don't forget to Star the Repo!
If you found this project helpful or inspiring, please consider giving it a ⭐ on GitHub!