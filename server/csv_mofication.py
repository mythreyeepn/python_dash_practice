import paramiko
import sqlite3
import os
import pandas as pd
from datetime import datetime

# Function to download a file from the SFTP server
def download_file_from_sftp(host, port, username, password, remote_file_path, local_file_path):
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Download the file to the local path
        sftp.get(remote_file_path, local_file_path)
        print(f"File downloaded successfully to {local_file_path}")
        
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Error: {e}")

# Function to create the SQLite database and table (if not exists)
def create_db_if_not_exists(db_path, csv_headers):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Dynamically create the table based on the headers from the CSV file
    columns_definition = ', '.join([f"{col} TEXT" for col in csv_headers])  # All columns as TEXT for simplicity
    create_table_query = f'''CREATE TABLE IF NOT EXISTS Ice_cds_open_interest (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_definition})'''
    
    cursor.execute(create_table_query)
    
    conn.commit()
    conn.close()

# Function to insert new data into the database dynamically based on the CSV headers
def insert_new_data(new_data, cursor, conn, csv_headers):
    placeholders = ', '.join(['?' for _ in csv_headers])
    insert_query = f"INSERT INTO Ice_cds_open_interest ({', '.join(csv_headers)}) VALUES ({placeholders})"
    
    for _, row in new_data.iterrows():
        cursor.execute(insert_query, row[csv_headers].tolist())
    
    conn.commit()

# Function to clean the CSV file (remove empty rows, trim spaces)
def clean_csv_data(df):
    # Remove any completely empty rows
    df = df.dropna(how='all')
    
    # Strip leading/trailing whitespaces from all string columns
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    return df

# Function to find missing records and insert new data into the SQLite DB
def process_csv(file_path, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read CSV into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Clean the CSV data
    df = clean_csv_data(df)

    # Extract headers from the CSV file
    csv_headers = list(df.columns)
    
    # Ensure the table exists with the same structure as the CSV headers
    create_db_if_not_exists(db_path, csv_headers)
    
    # Get existing records from the database
    existing_data = pd.read_sql_query(f"SELECT {', '.join(csv_headers)} FROM Ice_cds_open_interest", conn)
    
    # Find records in the CSV that are not in the existing data
    merged_data = df.merge(existing_data, on=csv_headers, how='left', indicator=True)
    new_records = merged_data[merged_data['_merge'] == 'left_only'].drop(columns=['_merge'])
    
    # Insert new records into the database
    if not new_records.empty:
        insert_new_data(new_records, cursor, conn, csv_headers)
        print(f"Inserted {len(new_records)} new records into the database.")
    else:
        print("No new records to insert.")
    
    conn.close()

# Function to check if today's file exists and process it
def check_and_process_file(local_file_path, db_path):
    if os.path.exists(local_file_path):
        process_csv(local_file_path, db_path)
    else:
        print(f"No file found for today: {local_file_path}")

# Paths for the SQLite DB
db_path = "y/codes/sqliteDB/ice_data.db"

# Mock SFTP credentials (replace with actual credentials)
sftp_host = "sftp.icewebsite.com"
sftp_port = 22
sftp_username = "your_username"
sftp_password = "your_password"

# Remote file path (no date in the remote file path)
remote_file = "/path/to/remote/ice_volume.csv"

# Get today's date to use in the local file name
today_date = datetime.today().strftime('%m_%d_%Y')

# Define the local file path with today's date
local_file = f"y/icedata/ice_volume_{today_date}.csv"

# Download the CSV file from the SFTP server (remote file without date, local file with today's date)
download_file_from_sftp(sftp_host, sftp_port, sftp_username, sftp_password, remote_file, local_file)

# Check if the file exists and process it if it does
check_and_process_file(local_file, db_path)
