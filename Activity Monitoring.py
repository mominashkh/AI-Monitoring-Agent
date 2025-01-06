import gradio as gr
import pandas as pd
import json
from datetime import datetime
from geopy.distance import geodesic

# Dummy data for demonstration purposes
sample_location_data = {
    "locations": [
        {"timestampMs": 1633072800000, "latitudeE7": 407128000, "longitudeE7": -740060000},
        {"timestampMs": 1633076400000, "latitudeE7": 407400000, "longitudeE7": -740500000},  # Farther from home
        {"timestampMs": 1633080000000, "latitudeE7": 407188000, "longitudeE7": -740100000},
    ]
}

sample_transaction_data = {
    "transactions": [
        {"timestamp": "2023-11-01T10:00:00Z", "amount": 100, "merchant": "Store A"},
        {"timestamp": "2023-11-01T12:00:00Z", "amount": 600, "merchant": "Store B"},
        {"timestamp": "2023-11-02T10:00:00Z", "amount": 50, "merchant": "Store C"},
    ]
}

# Function to process location data (simulated for demo)
def process_location_data(location_file):
    data = sample_location_data  # Using dummy data for demonstration
    locations = data.get('locations', [])
    df = pd.DataFrame(locations)
    df['timestamp'] = pd.to_datetime(df['timestampMs'], unit='ms')
    df['latitude'] = df['latitudeE7'] / 1e7
    df['longitude'] = df['longitudeE7'] / 1e7
    return df

# Detect unusual location activity (simulated)
def detect_unusual_locations(location_df, home_coords, threshold_km=20):
    location_df['distance_from_home'] = location_df.apply(
        lambda row: geodesic((row['latitude'], row['longitude']), home_coords).km, axis=1
    )
    unusual = location_df[location_df['distance_from_home'] > threshold_km]
    return unusual

# Process transaction data (simulated for demo)
def process_transaction_data(transaction_file):
    data = sample_transaction_data  # Using dummy data for demonstration
    transactions = data.get('transactions', [])
    df = pd.DataFrame(transactions)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# Detect suspicious transactions (simulated)
def detect_suspicious_transactions(transaction_df, spending_limit):
    suspicious = transaction_df[transaction_df['amount'] > spending_limit]
    return suspicious

# Gradio Interface Function
def run_analysis(threshold_km, spending_limit):
    try:
        # Fetch and process data
        location_df = process_location_data(None)
        transaction_df = process_transaction_data(None)

        # Analyze data
        unusual_locations = detect_unusual_locations(location_df, home_coords=(40.7128, -74.0060), threshold_km=threshold_km)  # Example: NYC coordinates
        suspicious_transactions = detect_suspicious_transactions(transaction_df, spending_limit=spending_limit)

        # Compile results
        alerts = []
        if not unusual_locations.empty:
            alerts.append(f"Unusual locations detected: {len(unusual_locations)} entries.")
        if not suspicious_transactions.empty:
            alerts.append(f"Suspicious transactions detected: {len(suspicious_transactions)} entries.")
        
        if alerts:
            return "\n".join(alerts)
        else:
            return "No unusual activities detected."
    
    except Exception as e:
        return f"An error occurred: {e}"

# Create Gradio Interface
def create_gradio_interface():
    interface = gr.Interface(
        fn=run_analysis,
        inputs=[
            gr.Slider(minimum=1, maximum=100, step=1, label="Threshold Distance (km)"),
            gr.Slider(minimum=0, maximum=1000, step=50, label="Spending Limit (USD)")
        ],
        outputs="text",
        live=True,
        title="AI Monitoring Agent Demo",
        description="This demo simulates an AI monitoring agent that detects unusual locations and suspicious transactions based on predefined thresholds. Adjust the sliders to change the detection thresholds."
    )
    
    interface.launch()

if __name__ == "__main__":
    create_gradio_interface()
