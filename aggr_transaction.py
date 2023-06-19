import json
import csv
import os

def aggregated_transaction(input_folder, output_file):
    # Initialize the CSV writer
    csv_writer = csv.writer(open(output_file, 'w', newline=''))

    # Write the CSV header
    csv_writer.writerow(
        ['State', 'Year', 'Transaction Category', 'Payment Instrument Type', 'Transaction Count', 'Transaction Amount'])

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
                        transaction_data = data['data']['transactionData']
                        for transaction_category in transaction_data:
                            category_name = transaction_category['name']
                            payment_instruments = transaction_category['paymentInstruments']
                            for payment_instrument in payment_instruments:
                                instrument_type = payment_instrument['type']
                                transaction_count = payment_instrument['count']
                                transaction_amount = payment_instrument['amount']
                                csv_writer.writerow(
                                    [state, year, category_name, instrument_type, transaction_count, transaction_amount])

    print("CSV conversion completed.")

# Example usage
input_folder = r"C:\Users\ELCOT\PycharmProjects\phonepe_pulse\pulse\data\aggregated\transaction\country\india\state"
output_file = r'D:\nehru\Class\Projects\aggregated_transaction.csv'

aggregated_transaction(input_folder, output_file)
