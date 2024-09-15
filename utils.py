import os
import json

UTM_DATA_FILE = 'utm_data.json'

# Function to load existing UTM data from utm_data.json
def load_utm_data():
    try:
        if os.path.exists(UTM_DATA_FILE):
            with open(UTM_DATA_FILE, 'r') as file:
                return json.load(file)
        return []
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading UTM data: {e}")
        return []

# Function to save UTM data to utm_data.json
def save_utm_data(data):
    try:
        with open(UTM_DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving UTM data: {e}")
