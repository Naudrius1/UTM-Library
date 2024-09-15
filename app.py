from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from admin import admin_bp, load_clients  # Import admin blueprint and load_clients from admin.py
from utils import load_utm_data, save_utm_data  # Import UTM functions from utils.py
import os

app = Flask(__name__)

# Enable CORS for your app
CORS(app)

# Set the secret key
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret')

@app.route('/')
def index():
    clients = load_clients()  # Load the clients and their campaigns from JSON
    return render_template('index.html', clients=clients)

# Route to handle UTM URL generation and save to JSON
@app.route('/submit', methods=['POST'])
def submit():
    try:
        client = request.form['client']
        campaign = request.form['campaign']
        source = request.form['source']
        medium = request.form['medium']
        term = request.form.get('term')  # Optional field
        content = request.form.get('content')  # Optional field

        # Construct the UTM URL only if parameters exist
        utm_url = f"?utm_source={source}&utm_medium={medium}&utm_campaign={campaign}"
        if term:
            utm_url += f"&utm_term={term}"
        if content:
            utm_url += f"&utm_content={content}"

        # Load existing UTM data
        utm_data = load_utm_data()

        # Add the new UTM entry
        new_entry = {
            'client': client,
            'source': source,
            'medium': medium,
            'campaign': campaign,
            'utm_url': utm_url
        }
        utm_data.append(new_entry)

        # Save the updated UTM data to the JSON file
        save_utm_data(utm_data)

        # Show success message and redirect to the UTM data page
        flash('UTM URL successfully generated and saved!', 'success')
        return redirect(url_for('view_utm_data'))

    except KeyError as e:
        flash(f"Missing required field: {e}", 'error')
        return redirect(url_for('index'))

# Route to view all UTM data in a table
@app.route('/utm-data', methods=['GET'])
def view_utm_data():
    # Load all UTM data from the JSON file
    utm_data = load_utm_data()

    # Get filter values from query parameters
    selected_client = request.args.get('client')
    selected_campaign = request.args.get('campaign')

    # Filter by client and campaign if selected
    if selected_client:
        utm_data = [entry for entry in utm_data if entry['client'] == selected_client]
    if selected_campaign:
        utm_data = [entry for entry in utm_data if entry['campaign'] == selected_campaign]

    # Collect unique clients and campaigns for the filter form
    clients = list(set([entry['client'] for entry in load_utm_data()]))
    campaigns = list(set([entry['campaign'] for entry in load_utm_data()]))

    # Pass the filtered UTM data, clients, and campaigns to the template
    return render_template('utm_data.html', utm_data=utm_data, clients=clients, campaigns=campaigns)

# Register the admin blueprint
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5500)
