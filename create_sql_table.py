import requests
import subprocess
import pandas as pd
import mysql.connector
import csv


# Clone the repository
# subprocess.run(["git", "clone", "https://github.com/phonepe/pulse.git"])

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@7890sql",
    database="phonepe"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Create the table
create_table_aggr_transaction = """
CREATE TABLE IF NOT EXISTS aggr_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    state VARCHAR(255),
    year INT,
    transaction_category VARCHAR(255),
    payment_instrument_type VARCHAR(255),
    transaction_count INT,
    transaction_amount FLOAT
)
"""
cursor.execute(create_table_aggr_transaction)
print("Table aggr_transaction created successfully.")

# Read data from the CSV file
csv_file = "D:/nehru/Class/Projects/aggregated_transaction.csv"
with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames
    print("CSV Headers:", headers)
    rows = list(reader)

# Insert values into the table
insert_query = """
INSERT INTO aggr_transaction (
    state, year, transaction_category, payment_instrument_type, transaction_count, transaction_amount
) VALUES (%s, %s, %s, %s, %s, %s)
"""
values = [
    (
        row["State"],
        int(row["Year"]),
        row["Transaction Category"],
        row["Payment Instrument Type"],
        int(row["Transaction Count"]),
        float(row["Transaction Amount"])
    )
    for row in rows
]
cursor.executemany(insert_query, values)
db.commit()
print("Data inserted successfully.")

# Create the table
create_table_aggr_user = """
CREATE TABLE IF NOT EXISTS aggr_user (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    state VARCHAR(255),
    year INT,
    brand VARCHAR(255),
    count INT,
    percentage FLOAT,
    registered_users INT,
    app_opens BIGINT
)
"""
cursor.execute(create_table_aggr_user)
print("Table aggr_user created successfully.")

# Read data from the CSV file
csv_file = "D:/nehru/Class/Projects/aggregated_user.csv"
with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames
    print("CSV Headers:", headers)
    rows = list(reader)

# Insert values into the table
insert_query = """
INSERT INTO aggr_user (
    state, year, brand, count, percentage, registered_users, app_opens
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
values = [
    (
        row["State"],
        int(row["Year"]),
        row["Brand"],
        int(row["Count"]),
        float(row["Percentage"]),
        int(row["Registered Users"]),
        int(row["App Opens"])
    )
    for row in rows
]
cursor.executemany(insert_query, values)
db.commit()
print("Data inserted successfully.")

# Create the table
create_table_map_transaction = """
CREATE TABLE IF NOT EXISTS map_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    state VARCHAR(255),
    year INT,
    district VARCHAR(255),
    pincode VARCHAR(255),
    transaction_category VARCHAR(255),
    transaction_count INT,
    transaction_amount FLOAT
)
"""
cursor.execute(create_table_map_transaction)
print("Table map_transaction created successfully.")

# Read data from the CSV file
csv_file = "D:/nehru/Class/Projects/map_transaction.csv"
with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames
    print("CSV Headers:", headers)
    rows = list(reader)

# Insert values into the table
insert_query = """
INSERT INTO map_transaction (
    state, year, district, pincode, transaction_category, transaction_count, transaction_amount
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
values = [
    (
        row["State"],
        int(row["Year"]),
        row["District"],
        row["Pincode"],
        row["Transaction Category"],
        int(row["Transaction Count"]),
        float(row["Transaction Amount"])
    )
    for row in rows
]
cursor.executemany(insert_query, values)
db.commit()
print("Data inserted successfully.")

# Create the table
create_table_map_user = """
CREATE TABLE IF NOT EXISTS map_user (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    state VARCHAR(255),
    year INT,
    district VARCHAR(255),
    pincode VARCHAR(255),
    registered_users INT
)
"""
cursor.execute(create_table_map_user)
print("Table map_user created successfully.")

# Read data from the CSV file
csv_file = "D:/nehru/Class/Projects/map_user.csv"
with open(csv_file, "r") as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames
    print("CSV Headers:", headers)
    rows = list(reader)

# Insert values into the table
insert_query = """
INSERT INTO map_user (
    state, year, district, pincode, registered_users
) VALUES (%s, %s, %s, %s, %s)
"""
values = [
    (
        row["State"],
        int(row["Year"]),
        row["District"],
        row["Pincode"],
        int(row["Registered Users"])
    )
    for row in rows
]
cursor.executemany(insert_query, values)
db.commit()
print("Data inserted successfully.")

# Close the cursor and database connection
cursor.close()
db.close()
