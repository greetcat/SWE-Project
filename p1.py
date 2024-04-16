from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Dictionary to store complaints (improved structure)
complaints = []
complaint_schema = {
    "id": 0,  # Unique ID for each complaint
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
    "supervisor": "supervisor",
    "admin": "admin"  # New admin credentials
}

# Global variables for available resources
available_manpower = 0
available_resources = 0

# Unique ID counter for complaints
complaint_id_counter = 1


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
        elif username == "admin":  # Redirect admin to admin.html
            return redirect(url_for('admin_dashboard'))
    else:
        # Incorrect credentials, redirect with error
        return redirect(url_for('index', error=True))


@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    global complaint_id_counter
    complaint_text = request.form['complaint']
    city = request.form['city']

    # Create new complaint with updated schema
    new_complaint = complaint_schema.copy()
    new_complaint["id"] = complaint_id_counter
    complaint_id_counter += 1  # Increment unique ID counter
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


@app.route('/verify_complaint/<int:complaint_id>', methods=['POST'])
def verify_complaint(complaint_id):
    global complaints
    complaint = next((c for c in complaints if c["id"] == complaint_id), None)
    if complaint:
        # Update status based on form submission
        complaint["status"] = "Verified" if request.form.get('verified') else "Submitted"
        complaint["verified_by"] = "clerk"  # Assuming current user is the clerk
        complaint["verified_at"] = datetime.datetime.now()

    return redirect(url_for('clerk_dashboard'))


@app.route('/schedule_complaint/<int:complaint_id>', methods=['POST'])
def schedule_complaint(complaint_id):  # Corrected function name
    global complaints
    complaint = next((c for c in complaints if c["id"] == complaint_id), None)
    if complaint:
        # Update status based on form submission
        complaint["status"] = "Scheduled" if request.form.get('scheduled') else "Submitted"
        complaint["scheduled_by"] = "admin"  # Assuming current user is the admin
        complaint["scheduled_at"] = datetime.datetime.now()

    return redirect(url_for('supervisor_dashboard'))  # Redirect to supervisor dashboard


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


@app.route('/assign_complaint/<int:complaint_id>', methods=['POST'])
def assign_complaint(complaint_id):
    global complaints
    complaint = next((c for c in complaints if c["id"] == complaint_id), None)
    if complaint:
        # Update status, assigned_to, and timestamp (optional)
        complaint["status"] = "Assigned"

    return redirect(url_for('supervisor_dashboard'))


@app.route('/update_priorities', methods=['POST'])
def update_priorities():
    new_priorities = request.form.getlist('priority')  # Get list of new priorities from form
    for complaint, new_priority in zip(complaints, new_priorities):
        complaint['priority'] = int(new_priority)  # Update priority for each complaint
    return redirect(url_for('supervisor_dashboard'))  # Redirect to supervisor dashboard

@app.route('/update_resources_manpower', methods=['POST'])
def update_resources_manpower():
    global raw_materials_count, machines_count, supervisor_count, clerk_count, worker_count, it_count, finance_count

    # Print the form data to debug
    print(request.form)

    category = request.form['category']
    subcategory = request.form['subcategory']
    new_value = int(request.form['new_value'])

    # Update the respective count based on category and subcategory
    if category == 'resources':
        if subcategory == 'raw_materials':
            # Update raw materials count
            raw_materials_count = new_value
        elif subcategory == 'machines':
            # Update machines count
            machines_count = new_value
    elif category == 'manpower':
        if subcategory == 'supervisors':
            # Update supervisors count
            supervisor_count = new_value
        elif subcategory == 'clerks':
            # Update clerks count
            clerk_count = new_value
        elif subcategory == 'workers':
            # Update workers count
            worker_count = new_value
        elif subcategory == 'it':
            # Update IT count
            it_count = new_value
        elif subcategory == 'finance':
            # Update finance count
            finance_count = new_value

    # Redirect to admin dashboard after updating counts
    return redirect(url_for('admin_dashboard'))


    # Initialize counts
supervisor_count = 12
clerk_count = 24
worker_count = 300
it_count = 5
finance_count = 3
raw_materials_count = 1000
machines_count = 40
@app.route('/admin_dashboard')
def admin_dashboard():


    # This route is for the admin dashboard
    return render_template('admin.html',
                           supervisor_count=supervisor_count,
                           clerk_count=clerk_count,
                           worker_count=worker_count,
                           it_count=it_count,
                           finance_count=finance_count,
                           raw_materials_count=raw_materials_count,
                           machines_count=machines_count)



@app.route('/contact')
def contact():
    # Render the contact.html template
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
