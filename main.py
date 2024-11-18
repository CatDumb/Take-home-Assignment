import argparse
import requests
import json
from collections import defaultdict

# Define the list of supplier URLs as a global variable
SUPPLIER_URLS = [
    "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme",
    "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia",
    "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies"
]

class Supplier:
    """Class to fetch data from a supplier URL."""
    
    def __init__(self, url):
        self.url = url
    
    def fetch(self, request_params):
        """Fetch data from the supplier URL with given request parameters."""
        try:
            response = requests.get(self.url, params=request_params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to fetch data from {self.url}: {e}")
            return []

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Fetch data from suppliers based on hotel and destination IDs.")
    parser.add_argument('hotel_ids', type=str, help="Comma-separated list of hotel IDs or 'none' if empty.")
    parser.add_argument('destination_ids', type=str, help="Comma-separated list of destination IDs or 'none' if empty.")
    args = parser.parse_args()
    
    hotel_ids = [id for id in args.hotel_ids.split(',') if id] if args.hotel_ids.lower() != 'none' else []
    destination_ids = [id for id in args.destination_ids.split(',') if id] if args.destination_ids.lower() != 'none' else []
    
    return hotel_ids, destination_ids

def merge_responses(aggregated_data, response):
    """Merge a single response into the aggregated data."""
    for entry in response:
        hotel_id = entry.get('hotel_id')
        destination_id = str(entry.get('destination_id'))  # Ensure destination_id is a string
        if hotel_id and destination_id:
            aggregated_data.append(entry)

def filter_aggregated_data(aggregated_data, hotel_ids, destination_ids):
    """Filter the aggregated data to include only entries that match all provided hotel_ids and destination_ids."""
    filtered_data = []
    for entry in aggregated_data:
        hotel_id = entry.get('hotel_id')
        destination_id = str(entry.get('destination_id'))  # Ensure destination_id is a string
        if hotel_id in hotel_ids and destination_id in destination_ids:
            filtered_data.append(entry)
    return filtered_data

def main():
    hotel_ids, destination_ids = parse_arguments()
    
    suppliers = [Supplier(url) for url in SUPPLIER_URLS]
    
    request_params = {
        "hotel_ids": hotel_ids,
        "destination_ids": destination_ids
    }
    
    aggregated_data = []
    for supplier in suppliers:
        response = supplier.fetch(request_params)
        merge_responses(aggregated_data, response)
    
    if not hotel_ids and not destination_ids:
        print(json.dumps(aggregated_data, indent=4))
    else:
        filtered_data = filter_aggregated_data(aggregated_data, hotel_ids, destination_ids)
        print(json.dumps(filtered_data, indent=4))

if __name__ == "__main__":
    main()