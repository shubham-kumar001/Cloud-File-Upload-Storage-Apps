from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import sqlite3
import uuid
import os

app = Flask(__name__)
app.secret_key = 'vehicle-rental-2024'

# Database setup
def init_db():
    conn = sqlite3.connect('rental.db')
    cursor = conn.cursor()
    
    # Users table - NO constraints for demo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            aadhar TEXT NOT NULL,
            driving_license TEXT NOT NULL,
            gender TEXT NOT NULL,
            location TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tickets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            ticket_id TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            purchase_date TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            booking_id TEXT NOT NULL,
            vehicle_category TEXT NOT NULL,
            vehicle_name TEXT NOT NULL,
            rental_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            price REAL NOT NULL,
            payment_method TEXT NOT NULL,
            booking_date TIMESTAMP NOT NULL,
            status TEXT DEFAULT 'confirmed',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# ALL VEHICLE CATEGORIES WITH PRICES (as per your requirements)
VEHICLE_CATEGORIES = {
    'commuter_bikes': {'12_hours': 550, '24_hours': 1000, 'name': 'Commuter Bikes'},
    'adventure_bikes': {'12_hours': 650, '24_hours': 1200, 'name': 'Adventure & Performance Bikes'},
    'royal_enfield_heritage': {'12_hours': 600, '24_hours': 1200, 'name': 'Royal Enfield Heritage & Classic'},
    'royal_enfield_adventure': {'12_hours': 700, '24_hours': 1400, 'name': 'Royal Enfield Adventure & Scrambler'},
    'royal_enfield_roadsters': {'12_hours': 850, '24_hours': 1800, 'name': 'Royal Enfield Roadsters & Sport'},
    'scooters': {'12_hours': 500, '24_hours': 1100, 'name': 'Scooters'},
    'hatchbacks': {'12_hours': 700, '24_hours': 1300, 'name': 'Hatchback Cars'},
    'sedans': {'12_hours': 760, '24_hours': 1600, 'name': 'Sedan Cars'},
    'suvs': {'12_hours': 1000, '24_hours': 2000, 'name': 'SUV Cars'},
    'minibus': {'per_day': 1100, 'name': 'Mini Bus'}
}

# COMPLETE VEHICLE LISTS (all your vehicles)
VEHICLES = {
    'commuter_bikes': [
        'Hero Splendor Plus Xtec',
        'Hero Splendor Plus',
        'Hero HF Deluxe',
        'Hero HF 100',
        'Hero Passion Pro Plus',
        'Hero Passion Pro',
        'Hero Glamour Xtec',
        'Hero Glamour',
        'Hero Super Splendor Xtec',
        'Hero Super Splendor'
    ],
    'adventure_bikes': [
        'Hero Xtreme 125R',
        'Hero Xtreme 160R 4V',
        'Hero XPulse 200 4V',
        'Hero XPulse 210',
        'Hero Karizma XMR',
        'Hero Mavrick 440',
        'Hero Xtreme 250R'
    ],
    'royal_enfield_heritage': [
        'Classic 350',
        'Bullet 350',
        'Classic 650'
    ],
    'royal_enfield_adventure': [
        'Meteor 350',
        'Super Meteor 650',
        'Himalayan 450',
        'Scram 411'
    ],
    'royal_enfield_roadsters': [
        'Hunter 350',
        'Interceptor 650',
        'Continental GT 650',
        'Guerrilla 450'
    ],
    'scooters': [
        'Hero Pleasure Plus',
        'Hero Maestro Edge 110',
        'Hero Maestro Edge 125',
        'Hero Xoom 125',
        'Hero Xoom 160'
    ],
    'hatchbacks': [
        'Maruti Suzuki Swift',
        'Maruti Suzuki Dzire',
        'Hyundai i10',
        'Hyundai i20',
        'Maruti Wagon R',
        'Maruti Celerio'
    ],
    'sedans': [
        'Honda City',
        'Hyundai Verna',
        'Hyundai Aura',
        'Toyota Etios',
        'Maruti Ciaz'
    ],
    'suvs': [
        'Hyundai Creta',
        'Mahindra Scorpio-N',
        'Mahindra XUV500',
        'Toyota Innova Crysta'
    ],
    'minibus': [
        'Ford Transit',
        'Mercedes-Benz Sprinter',
        'Toyota Coaster',
        'Force Traveller',
        'Tata Winger',
        'Tata Starbus',
        'Mahindra Tourister',
        'Mahindra Cruzio'
    ]
}

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile = request.form['mobile']
        aadhar = request.form['aadhar']
        
        conn = sqlite3.connect('rental.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE mobile = ?', (mobile,))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            session['name'] = user[1]
            # Check if user has ticket
            cursor.execute('SELECT * FROM tickets WHERE user_id = ?', (user[0],))
            ticket = cursor.fetchone()
            if ticket:
                session['has_ticket'] = True
                session['ticket_id'] = ticket[2]
            return redirect(url_for('dashboard'))
        else:
            flash('User not found. Please register first.', 'error')
            return redirect(url_for('register'))
    
    return render_template('login.html')

# In app.py, update the register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        aadhar = request.form['aadhar']
        driving_license = request.form['driving_license']
        gender = request.form['gender']
        location = request.form['location']
        latitude = request.form.get('latitude', '')
        longitude = request.form.get('longitude', '')
        
        # Store in database with location data
        conn = sqlite3.connect('rental.db')
        cursor = conn.cursor()
        
        # Update users table to include coordinates
        cursor.execute('''
            ALTER TABLE users ADD COLUMN latitude TEXT DEFAULT '';
        ''')
        cursor.execute('''
            ALTER TABLE users ADD COLUMN longitude TEXT DEFAULT '';
        ''')
        
        cursor.execute('''
            INSERT INTO users (name, mobile, aadhar, driving_license, gender, location, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, mobile, aadhar, driving_license, gender, location, latitude, longitude))
        
        conn.commit()
        cursor.execute('SELECT id FROM users WHERE mobile = ?', (mobile,))
        user = cursor.fetchone()
        conn.close()
        
        session['user_id'] = user[0]
        session['name'] = name
        session['location'] = location
        session['latitude'] = latitude
        session['longitude'] = longitude
        
        return redirect(url_for('ticket'))
    
    return render_template('register.html')

@app.route('/ticket', methods=['GET', 'POST'])
def ticket():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Create ticket
        ticket_id = str(uuid.uuid4())[:8].upper()
        
        conn = sqlite3.connect('rental.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickets (user_id, ticket_id, amount, payment_method, purchase_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['user_id'], ticket_id, 20, 'cash', datetime.now()))
        conn.commit()
        conn.close()
        
        session['has_ticket'] = True
        session['ticket_id'] = ticket_id
        return redirect(url_for('dashboard'))
    
    return render_template('payment.html', amount=20, description="Entry Ticket", ticket=True)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if not session.get('has_ticket'):
        return redirect(url_for('ticket'))
    
    return render_template('dashboard.html', name=session.get('name'))

@app.route('/vehicles')
def vehicles():
    if 'user_id' not in session or not session.get('has_ticket'):
        return redirect(url_for('login'))
    
    return render_template('vehicles.html', 
                         categories=VEHICLE_CATEGORIES,
                         vehicles=VEHICLES)

@app.route('/book/<category>', methods=['GET', 'POST'])
def book_vehicle(category):
    if 'user_id' not in session or not session.get('has_ticket'):
        return redirect(url_for('login'))
    
    if category not in VEHICLE_CATEGORIES:
        return redirect(url_for('vehicles'))
    
    if request.method == 'POST':
        vehicle_name = request.form['vehicle']
        rental_type = request.form.get('rental_type', '12_hours')
        start_date = request.form['start_date']
        
        # Calculate price
        price = 0
        if category == 'minibus':
            days = int(request.form.get('days', 1))
            price = VEHICLE_CATEGORIES[category]['per_day'] * days
            rental_type = f"{days} day(s)"
        else:
            if rental_type == '12_hours':
                price = VEHICLE_CATEGORIES[category]['12_hours']
            else:
                price = VEHICLE_CATEGORIES[category]['24_hours']
        
        # Save booking to session
        session['booking'] = {
            'category': category,
            'vehicle': vehicle_name,
            'rental_type': rental_type,
            'start_date': start_date,
            'price': price
        }
        
        return redirect(url_for('booking_payment'))
    
    return render_template('booking.html',
                         category=category,
                         category_name=VEHICLE_CATEGORIES[category]['name'],
                         vehicles=VEHICLES[category],
                         is_minibus=(category == 'minibus'),
                         categories=VEHICLE_CATEGORIES)

@app.route('/booking-payment', methods=['GET', 'POST'])
def booking_payment():
    if 'user_id' not in session or not session.get('has_ticket'):
        return redirect(url_for('login'))
    
    if 'booking' not in session:
        return redirect(url_for('vehicles'))
    
    booking = session['booking']
    
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        
        # Generate booking ID
        booking_id = str(uuid.uuid4())[:8].upper()
        
        # Save to database
        conn = sqlite3.connect('rental.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (user_id, booking_id, vehicle_category, vehicle_name, 
                                rental_type, start_date, price, payment_method, booking_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], booking_id, booking['category'], booking['vehicle'],
              booking['rental_type'], booking['start_date'], booking['price'],
              payment_method, datetime.now()))
        conn.commit()
        conn.close()
        
        session['booking_id'] = booking_id
        return redirect(url_for('confirmation'))
    
    return render_template('payment.html', 
                         amount=booking['price'],
                         description=f"Booking for {booking['vehicle']}",
                         ticket=False)

@app.route('/confirmation')
def confirmation():
    if 'user_id' not in session or 'booking_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('rental.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM bookings WHERE booking_id = ? AND user_id = ?
    ''', (session['booking_id'], session['user_id']))
    booking = cursor.fetchone()
    conn.close()
    
    if not booking:
        return redirect(url_for('dashboard'))
    
    return render_template('confirmation.html', booking=booking)
# Add this route to app.py
@app.route('/nearby-vehicles')
def nearby_vehicles():
    if 'user_id' not in session or not session.get('has_ticket'):
        return redirect(url_for('login'))
    
    user_lat = session.get('latitude')
    user_lng = session.get('longitude')
    
    # In a real app, you would query vehicles near the user's location
    # For demo, we'll show all vehicles with distance simulation
    
    return render_template('nearby_vehicles.html',
                         name=session.get('name'),
                         location=session.get('location'),
                         categories=VEHICLE_CATEGORIES,
                         vehicles=VEHICLES,
                         user_lat=user_lat,
                         user_lng=user_lng)
@app.route('/thankyou')
def thankyou():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Clear booking session
    session.pop('booking', None)
    session.pop('booking_id', None)
    
    return render_template('thankyou.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Delete old database and start fresh
    if os.path.exists('rental.db'):
        os.remove('rental.db')
    init_db()
    print("✅ Database reset complete!")
    print("✅ Vehicle lists loaded with ALL categories:")
    for category, vehicles in VEHICLES.items():
        print(f"   - {category}: {len(vehicles)} vehicles")
    app.run(debug=True, port=5000)
