from flask import Blueprint, render_template, request, flash, jsonify
from utils import load_utm_data  # Import the UTM data loader from utils.py
import json
import os

# Define the blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

CLIENTS_FILE = 'clients.json'

# Load JSON data for clients and campaigns
def load_clients():
    if os.path.exists(CLIENTS_FILE):
        try:
            with open(CLIENTS_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # Handle invalid JSON format in clients.json
            print("Error: Failed to decode JSON from clients.json.")
            return {}
    print("Error: clients.json file not found.")
    return {}

# Save JSON data for clients and campaigns
def save_clients(data):
    try:
        with open(CLIENTS_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError:
        print("Error: Failed to save data to clients.json.")

# Admin page route (client/campaign management)
@admin_bp.route('/', methods=['GET', 'POST'])
def admin():
    clients = load_clients()

    if request.method == 'POST':
        if 'add_client' in request.form:
            new_client = request.form['client_name'].strip()
            if new_client and new_client not in clients:
                clients[new_client] = []
                save_clients(clients)
                flash(f'Client {new_client} added successfully!', 'success')
            else:
                flash('Client already exists or invalid name.', 'danger')

        elif 'add_campaign' in request.form:
            client_name = request.form['client_select'].strip()
            new_campaign = request.form['campaign_name'].strip()
            if client_name in clients and new_campaign:
                if new_campaign not in clients[client_name]:  # Prevent duplicate campaigns
                    clients[client_name].append(new_campaign)
                    save_clients(clients)
                    flash(f'Campaign {new_campaign} added to {client_name}!', 'success')
                else:
                    flash('Campaign already exists for this client.', 'danger')
            else:
                flash('Invalid client or campaign name.', 'danger')
        
        elif 'delete_client' in request.form:
            client_to_delete = request.form['client_select'].strip()
            if client_to_delete in clients:
                del clients[client_to_delete]
                save_clients(clients)
                flash(f'Client {client_to_delete} deleted.', 'success')
            else:
                flash(f'Client {client_to_delete} not found.', 'danger')
        
        elif 'delete_campaign' in request.form:
            client_name = request.form['client_select'].strip()
            campaign_to_delete = request.form['campaign_select'].strip()
            if client_name in clients and campaign_to_delete in clients[client_name]:
                clients[client_name].remove(campaign_to_delete)
                save_clients(clients)
                flash(f'Campaign {campaign_to_delete} deleted from {client_name}.', 'success')
            else:
                flash(f'Campaign or client not found.', 'danger')

    return render_template('admin.html', clients=clients)

# API route to get campaigns for a client
@admin_bp.route('/get_campaigns/<client>')
def get_campaigns(client):
    clients = load_clients()  # Load JSON data
    campaigns = clients.get(client, [])  # Get campaigns for the selected client
    return jsonify(campaigns)  # Return campaigns as JSON

# Add UTM Data route
@admin_bp.route('/utm-data')
def utm_data():
    utm_data = load_utm_data()  # Load UTM data using the utility function
    return render_template('utm_data.html', utm_data=utm_data)
