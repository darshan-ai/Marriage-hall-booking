from flask import Flask, render_template, request, redirect, url_for, flash
from replit import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    try:
        full_name = request.args.get('full_name')
        booking_data = None
        if full_name:
            booking_data = db.get(full_name)
        return render_template('index.html', booking_data=booking_data)
    except Exception as e:
        print(f"Error in index route: {e}")
        flash(f"An error occurred: {e}")
        return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        full_name = f"{first_name} {last_name}"
        hall_name = request.form['hall_name']
        booking_date = request.form['booking_date']
        booking_time = request.form['booking_time']
        num_guests = request.form['num_guests']

        db[full_name] = {
            'first_name': first_name,
            'last_name': last_name,
            'hall_name': hall_name,
            'booking_date': booking_date,
            'booking_time': booking_time,
            'num_guests': num_guests
        }

        flash(f"Booking for {full_name} on {booking_date} at {hall_name} has been successfully saved.")
    except Exception as e:
        flash(f"An error occurred: {e}")

    return redirect(url_for('index'))

@app.route('/retrieve', methods=['GET'])
def retrieve():
    try:
        full_name = request.args.get('full_name')
        return redirect(url_for('index', full_name=full_name))
    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('index'))

@app.route('/delete/<full_name>', methods=['POST'])
def delete(full_name):
    try:
        if full_name in db:
            del db[full_name]
            flash(f"Booking for {full_name} has been successfully deleted.")
        else:
            flash(f"Booking for {full_name} not found.")
    except Exception as e:
        flash(f"An error occurred: {e}")
    return redirect(url_for('index'))

@app.route('/modify/<full_name>', methods=['POST'])
def modify(full_name):
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        hall_name = request.form['hall_name']
        booking_date = request.form['booking_date']
        booking_time = request.form['booking_time']
        num_guests = request.form['num_guests']

        if full_name in db:
            db[full_name] = {
                'first_name': first_name,
                'last_name': last_name,
                'hall_name': hall_name,
                'booking_date': booking_date,
                'booking_time': booking_time,
                'num_guests': num_guests
            }
            flash(f"Booking for {full_name} has been successfully modified.")
        else:
            flash(f"Booking for {full_name} not found.")
    except Exception as e:
        flash(f"An error occurred: {e}")
    return redirect(url_for('index', full_name=full_name))

@app.route('/view_bookings')
def view_bookings():
    try:
        bookings = {key: db[key] for key in db.keys()}
        return render_template('view_bookings.html', bookings=bookings)
    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('index'))

@app.route('/calendar_view')
def calendar_view():
    try:
        bookings = {}
        for full_name, booking in db.items():
            hall = booking['hall_name']
            if hall not in bookings:
                bookings[hall] = []
            bookings[hall].append(booking['booking_date'])

        return render_template('calendar_view.html', bookings=bookings)
    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
