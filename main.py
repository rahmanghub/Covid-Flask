import json
# from flask_login import login_required
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'it%z^secret^'

# File path to store user data
USER_DATA_FILE = 'users_different.json'

# Load user data from JSON file
def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user data to JSON file
def save_user_data(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)

# Create a dictionary to store user information
users = load_user_data()

# User login
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the provided email and password match a user in the dictionary
        if email in users and users[email]['password'] == password:
            session['email'] = email
            return redirect(url_for('user_profile'))  # Redirect to user profile page
        else:
            error_message = "Invalid email or password. Please try again."
            return render_template('signin.html', error_message=error_message)

    return render_template('signin.html')


# User signup
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if the email is already registered
        if email in users:
            error_message = "Email already registered. Please use a different email."
            return render_template('register.html', error_message=error_message)

        # Store the user information in the dictionary
        users[email] = {'name': name, 'password': password}
        save_user_data(users)  # Save user data to JSON file

        return redirect(url_for('signin'))

    return render_template('register.html')


# Admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    #     # Validate admin credentials
    #     if username == admin_username and password == admin_password:
    #         session['admin'] = True
    #         return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
    #     else:
    #         error_message = "Invalid admin credentials. Please try again."
    #         return render_template('admin.html', error_message=error_message)

    # return render_template('admin.html')

# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    # Check if the user is an admin
    if session.get('admin'):
        # Get dosage details grouped by vaccination centers
        dosage_details = get_dosage_details()

        return render_template('admin_dashboard.html', dosage_details=dosage_details)
    else:
        return redirect(url_for('admin'))  # Redirect to admin login

# Function to get dosage details grouped by vaccination centers
def get_dosage_details():
    dosage_details = [
        {
            'center_name': 'Vaccination Center 1',
            'dosage_count': 100
        },
        {
            'center_name': 'Vaccination Center 2',
            'dosage_count': 80
        },
    ]
    return dosage_details

# VaccinationCenter class
class VaccinationCenter:
    def __init__(self, name, working_hours):
        self.name = name
        self.working_hours = working_hours

    def get_details(self):
        return {
            'name': self.name,
            'working_hours': self.working_hours
        }

# List to store vaccination centers
vaccination_centers = []

# Admin dashboard - Add Vaccination Centers
@app.route('/admin/add-center', methods=['POST'])
def add_center():
    name = request.form['name']
    working_hours = request.form['working_hours']

    center = VaccinationCenter(name, working_hours)
    vaccination_centers.append(center)

    return redirect(url_for('admin_dashboard'))

# Admin dashboard - Remove Vaccination Centers
@app.route('/admin/remove-center/<int:index>')
def remove_center(index):
    if 0 <= index < len(vaccination_centers):
        vaccination_centers.pop(index)

    return redirect(url_for('admin_dashboard'))

# User profile - Display Vaccination Centers (with login required)
@app.route('/user', methods=['GET', 'POST'])
# @login_required
def user_profile():
    # Get the current user information from the session
    email = session.get('email')
    user = users.get(email)

    if user:
        return render_template('user_profile.html', user=user, vaccination_centers=vaccination_centers)
    else:
        return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(host="0.0.0.0")
