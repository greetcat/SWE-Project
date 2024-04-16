# from flask import Flask, render_template, request, redirect, url_for
#
# app = Flask(__name__)
#
# # Dictionary to store complaints
# complaints = []
#
# # Dictionary to store verified complaints
# verified_complaints = {}
#
# # Dictionary to store user credentials
# user_credentials = {
#     "clerk": "clerk",
#     "supervisor": "supervisor"
# }
#
# # Global variables for available manpower and resources
# available_manpower = 0
# available_resources = 0
#
#
# @app.route('/')
# def index():
#     error = request.args.get('error', False)
#     return render_template('index.html', error=error)
#
#
# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
#
#     if username in user_credentials and user_credentials[username] == password:
#         # Redirect to dashboard for clerk or supervisor
#         if username == "clerk":
#             return redirect(url_for('clerk_dashboard'))
#         elif username == "supervisor":
#             return redirect(url_for('supervisor_dashboard'))
#     else:
#         # Incorrect username or password, redirect back to index with an error message
#         return redirect(url_for('index', error=True))
#
#
# @app.route('/submit_complaint', methods=['POST'])
# def submit_complaint():
#     complaint = request.form['complaint']
#     city = request.form['city']
#
#     # Add the complaint to the list of complaints with priority 0 and status "Submitted"
#     complaints.append({"complaint": complaint, "city": city, "status": "Submitted", "priority": 0})
#
#     return redirect(url_for('dashboard'))
#
#
# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html', complaints=complaints)
#
#
# @app.route('/clerk_dashboard')
# def clerk_dashboard():
#     return render_template('clerk_dashboard.html', complaints=complaints)
#
#
# @app.route('/verify_complaint/<int:index>')
# def verify_complaint(index):
#     if index < len(complaints):
#         complaints[index]['status'] = 'Verified'
#
#     return redirect(url_for('dashboard'))
#
#
# @app.route('/supervisor_dashboard', methods=['GET', 'POST'])
# def supervisor_dashboard():
#     global available_manpower, available_resources
#
#     if request.method == 'POST':
#         # Update available manpower and resources
#         available_manpower = int(request.form['available_manpower'])
#         available_resources = int(request.form['available_resources'])
#
#     # Pass complaints with priorities to the template
#     return render_template('supervisor_dashboard.html', complaints=complaints,
#                            available_manpower=available_manpower, available_resources=available_resources)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for
import datetime  # Import datetime for timestamps

app = Flask(__name__)

# Dictionary to store complaints (improved structure)
complaints = []
complaint_schema = {
    "complaint_text": "",
    "city": "",
    "status": "Submitted",  # Default status
    "priority": 0,
    "verified_by": None,  # Track verification (clerk)
    "verified_at": None,  # Timestamp for verification
    "assigned_to": None,  # Track assignment (supervisor)
    "assigned_at": None,  # Timestamp for assignment
    "start_date": None,  # Track repair start (optional)
    "end_date": None,  # Track repair completion (optional)
}

# User credentials
user_credentials = {
    "clerk": "clerk",
    "supervisor": "supervisor"
}

# Global variables for available resources
available_manpower = 0
available_resources = 0


@app.route('/')
def index():
    error = request.args.get('error', False)
    return render_template('index.html', error=error)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in user_credentials and user_credentials[username] == password:
        # Redirect to appropriate dashboard
        if username == "clerk":
            return redirect(url_for('clerk_dashboard'))
        elif username == "supervisor":
            return redirect(url_for('supervisor_dashboard'))
    else:
        # Incorrect credentials, redirect with error
        return redirect(url_for('index', error=True))


@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    complaint_text = request.form['complaint']
    city = request.form['city']

    # Create new complaint with updated schema
    new_complaint = complaint_schema.copy()
    new_complaint["complaint_text"] = complaint_text
    new_complaint["city"] = city
    complaints.append(new_complaint)

    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', complaints=complaints)



@app.route('/clerk_dashboard')
def clerk_dashboard():
    return render_template('clerk_dashboard.html', complaints=complaints)


@app.route('/verify_complaint/<int:index>', methods=['POST'])
def verify_complaint(index):
    if index < len(complaints):
        complaint = complaints[index]
        # Update status based on form submission
        complaint["status"] = "Verified" if request.form.get('verified') else "Submitted"
        complaint["verified_by"] = "clerk"  # Assuming current user is the clerk
        complaint["verified_at"] = datetime.datetime.now()

    return redirect(url_for('clerk_dashboard'))



@app.route('/reject_complaint/<int:index>', methods=['POST'])
def reject_complaint(index):
    if index < len(complaints):
        complaint = complaints[index]
        # Update status to "Rejected" (add logic for reason if needed)
        complaint["status"] = "Rejected"

    return redirect(url_for('clerk_dashboard'))


@app.route('/supervisor_dashboard', methods=['GET', 'POST'])
def supervisor_dashboard():
    global available_manpower, available_resources

    if request.method == 'POST':
        # Update available resources
        available_manpower = int(request.form['available_manpower'])
        available_resources = int(request.form['available_resources'])

    # Pass complaints with additional tracking information
    return render_template('supervisor_dashboard.html', complaints=complaints,
                          available_manpower=available_manpower,
                          available_resources=available_resources)


@app.route('/assign_complaint/<int:index>', methods=['POST'])
def assign_complaint(index):
    if index < len(complaints):
        complaint = complaints[index]
        # Update status, assigned_to, and timestamp (optional)
        complaint["status"] = "Assigned"


if __name__ == '__main__':
    app.run(debug=True)
