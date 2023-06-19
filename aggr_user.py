import json
import csv
import os

def extract_data_from_json(json_data, output_file, state, year):
    # Verify if json_data is None
    if json_data is None:
        print(f"JSON data is None for state {state} and year {year}. Skipping...")
        return

    # Extract the relevant data from the JSON structure
    # Open the CSV file in append mode
    with open(output_file, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Extract the data from the JSON structure
        data = json_data.get('data', {}).get('usersByDevice')

        if data is None:
            data = []  # Set an empty list if data is None

        registered_users = json_data.get('data', {}).get('aggregated', {}).get('registeredUsers')
        app_opens = json_data.get('data', {}).get('aggregated', {}).get('appOpens')

        for item in data:
            brand = item['brand']
            count = item['count']
            percentage = item['percentage']
            csv_writer.writerow([state, year, brand, count, percentage, registered_users, app_opens])

    print("CSV conversion completed.")

def process_json_files(input_folder, output_file):
    # Open the CSV file and write the header
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['State', 'Year', 'Brand', 'Count', 'Percentage', 'Registered Users', 'App Opens'])

        # Traverse through each state folder
        for state_folder in os.listdir(input_folder):
            state_path = os.path.join(input_folder, state_folder)

            # Check if it is a directory
            if not os.path.isdir(state_path):
                continue

            # Extract the state name
            state = state_folder

            # Traverse through each year folder inside the state folder
            for year_folder in os.listdir(state_path):
                year_path = os.path.join(state_path, year_folder)

                # Check if it is a directory
                if not os.path.isdir(year_path):
                    continue

                # Extract the year
                year = year_folder

                # Traverse through each JSON file inside the year folder
                for file in os.listdir(year_path):
                    if file.endswith(".json"):
                        json_file_path = os.path.join(year_path, file)
                        with open(json_file_path) as json_file:
                            data = json.load(json_file)
                            extract_data_from_json(data, output_file, state, year)

    print("CSV conversion completed.")

# Example usage
input_folder = r"C:\Users\ELCOT\PycharmProjects\phonepe_pulse\pulse\data\aggregated\user\country\india\state"
output_file = r"D:\nehru\Class\Projects\aggregated_user.csv"

# Process the JSON files in the input folder
process_json_files(input_folder, output_file)
