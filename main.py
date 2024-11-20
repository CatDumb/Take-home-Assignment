import argparse
import requests
import json
from collections import defaultdict

def is_substring(str1, str2):
    """Check if str1 is a substring of str2 or vice versa, or if they contain the same words in different orders."""
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    return set1 == set2 or str1 in str2 or str2 in str1

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

class Hotel:
    """Class to store hotel data."""
    
    def __init__(self, hotel_id, destination_id, location):
        self.hotel_id = hotel_id
        self.destination_id = destination_id
        self.location = location

    def merge(self, new_entry):
        """Merge new entry data into the existing hotel data."""
        for key, value in new_entry.items():
            # Check if the key exists in the current hotel data
            if key in self.__dict__:
                # If the value is a list, merge the lists without duplicates
                if isinstance(self.__dict__[key], list):
                    for item in value:
                        if not any(is_substring(str(item), str(existing_item)) for existing_item in self.__dict__[key]):
                            self.__dict__[key].append(item)
                # If the value is a string, concatenate the strings if not already a substring
                elif isinstance(self.__dict__[key], str):
                    if not is_substring(str(self.__dict__[key]), str(value)):
                        self.__dict__[key] += ' ' + str(value)
                # For other types, replace the existing value with the new value if they are not identical
                else:
                    if self.__dict__[key] != value:
                        self.__dict__[key] = value
            else:
                # Check if the new key is a substring of any existing key or vice versa
                existing_key = next((k for k in self.__dict__ if is_substring(k, key) or is_substring(key, k)), None)
                if existing_key:
                    # If the value is a list, merge the lists without duplicates
                    if isinstance(self.__dict__[existing_key], list):
                        for item in value:
                            if not any(is_substring(str(item), str(existing_item)) for existing_item in self.__dict__[existing_key]):
                                self.__dict__[existing_key].append(item)
                    # If the value is a string, concatenate the strings if not already a substring
                    elif isinstance(self.__dict__[existing_key], str):
                        if not is_substring(str(self.__dict__[existing_key]), str(value)):
                            self.__dict__[existing_key] += ' ' + str(value)
                    # For other types, replace the existing value with the new value if they are not identical
                    else:
                        if self.__dict__[existing_key] != value:
                            self.__dict__[existing_key] = value
                else:
                    # If no matching key is found, add the new key-value pair
                    self.__dict__[key] = value

    @staticmethod
    def from_entry(entry):
        """Create a Hotel object from a single entry."""
        entry_items = list(entry.items())
        hotel_id = str(entry_items[0][1])  # Extract the value of the first item
        destination_id = str(entry_items[1][1])  # Extract the value of the second item
        return Hotel(
            hotel_id=hotel_id,
            destination_id=destination_id,
            location=entry.get('location', {})
        )

def merge_responses(hotels, response):
    """Merge a single response into the hotels array."""
    for entry in response:
        # Extract hotel_id and destination_id from the first and second fields
        entry_items = list(entry.items())
        hotel_id = str(entry_items[0][1])  # Ensure hotel_id is a string
        destination_id = str(entry_items[1][1])  # Ensure destination_id is a string
        
        print(f"Processing entry: hotel_id={hotel_id}, destination_id={destination_id}")
        
        if hotel_id and destination_id:
            # Check if the hotel already exists in the hotels array
            existing_hotel = next((hotel for hotel in hotels if hotel.hotel_id == hotel_id and hotel.destination_id == destination_id), None)
            if existing_hotel:
                print(f"Merging with existing hotel: {existing_hotel.hotel_id}, {existing_hotel.destination_id}")
                # Merge the new entry with the existing hotel data
                existing_hotel.merge(entry)
            else:
                print(f"Creating new hotel entry: {hotel_id}, {destination_id}")
                # Create a new Hotel object and add it to the hotels array
                new_hotel = Hotel.from_entry(entry)
                hotels.append(new_hotel)
        else:
            print(f"Skipping entry: hotel_id={hotel_id}, destination_id={destination_id} (missing hotel_id or destination_id)")

def filter_aggregated_data(hotels, hotel_ids, destination_ids):
    """Filter the aggregated data to include only entries that match all provided hotel_ids and destination_ids."""
    filtered_data = []
    for hotel in hotels:
        if hotel.hotel_id in hotel_ids and hotel.destination_id in destination_ids:
            filtered_data.append(hotel)
    return filtered_data

def main():
    hotel_ids, destination_ids = parse_arguments()
    
    suppliers = [Supplier(url) for url in SUPPLIER_URLS]
    
    request_params = {
        "hotel_ids": hotel_ids,
        "destination_ids": destination_ids
    }
    
    hotels = []
    for supplier in suppliers:
        response = supplier.fetch(request_params)
        merge_responses(hotels, response)
    
    if not hotel_ids and not destination_ids:
        print(json.dumps([hotel.__dict__ for hotel in hotels], indent=4))
    else:
        filtered_hotels = filter_aggregated_data(hotels, hotel_ids, destination_ids)
        print(json.dumps([hotel.__dict__ for hotel in filtered_hotels], indent=4))

if __name__ == "__main__":
    main()