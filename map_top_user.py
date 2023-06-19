import json
import csv
import os

def map_user(input_folder, output_file):
    # Initialize the CSV writer
    csv_writer = csv.writer(open(output_file, 'w', newline=''))

    # Write the CSV header
    csv_writer.writerow(['State', 'Year', 'District', 'Pincode', 'Registered Users'])

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

                        # Extract data from the JSON structure
                        districts = data['data']['districts']
                        for district in districts:
                            district_name = district['name']
                            registered_users = district['registeredUsers']
                            csv_writer.writerow([state, year, district_name, '', registered_users])

                        pincodes = data['data']['pincodes']
                        for pincode in pincodes:
                            pincode_name = pincode['name']
                            registered_users = pincode['registeredUsers']
                            csv_writer.writerow([state, year, '', pincode_name, registered_users])

    print("CSV conversion completed.")

# Example usage
input_folder = r"C:\Users\ELCOT\PycharmProjects\phonepe_pulse\pulse\data\top\user\country\india\state"
output_file = r'D:\nehru\Class\Projects\map_user.csv'

map_user(input_folder, output_file)
