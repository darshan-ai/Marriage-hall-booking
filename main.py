from flask import Flask, render_template, request, redirect, url_for, flash
from replit import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    # Rendering the index page (formerly home)
    return render_template('index.html')

@app.route('/book_hall', methods=['GET', 'POST'])
def book_hall():
    if request.method == 'POST':
        try:
            # Collect booking details from the form
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            full_name = f"{first_name} {last_name}"
            hall_name = request.form['hall_name']
            booking_date = request.form['booking_date']
            booking_time = request.form['booking_time']
            num_guests = request.form['num_guests']

            # Save booking to database
            db[full_name] = {
                'first_name': first_name,
                'last_name': last_name,
                'hall_name': hall_name,
                'booking_date': booking_date,
                'booking_time': booking_time,
                'num_guests': num_guests
            }

            # Flash success message and redirect to index page
            flash(f"Booking for {full_name} on {booking_date} at {hall_name} has been successfully saved.")
            return redirect(url_for('index'))
        except Exception as e:
            # Handle errors and show an error message
            flash(f"An error occurred: {e}")
            return redirect(url_for('book_hall'))
    # Render the book hall page
    return render_template('book_hall.html')

@app.route('/retrieve_booking', methods=['GET', 'POST'])
def retrieve_booking():
    booking_data = None
    if request.method == 'POST':
        # Retrieve booking based on full name
        full_name = request.form['full_name']
        booking_data = db.get(full_name)
        if not booking_data:
            # Flash error if booking not found
            flash(f"No booking found for {full_name}.")
    # Render the retrieve booking page and pass any found booking data
    return render_template('retrieve_booking.html', booking_data=booking_data)

@app.route('/view_bookings')
def view_bookings():
    # Fetch all bookings from the database
    bookings = {key: db[key] for key in db.keys()}
    # Render the view bookings page and pass the booking data
    return render_template('view_bookings.html', bookings=bookings)

@app.route('/calendar_view')
def calendar_view():
    bookings = {}
    # Populate bookings per hall for calendar view
    for full_name, booking in db.items():
        hall = booking['hall_name']
        booking_date = booking['booking_date']

        # Group bookings by hall name
        if hall not in bookings:
            bookings[hall] = []
        bookings[hall].append(booking_date)

    # Render the calendar view and pass the booking data
    return render_template('calendar_view.html', bookings=bookings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
