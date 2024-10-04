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
def create_db_if_not_exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Ice_cds_open_interest (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        col1 TEXT,
                        col2 TEXT,
                        col3 REAL
                     )''')
    
    conn.commit()
    conn.close()

# Function to insert new data into the database
def insert_new_data(new_data, cursor, conn):
    for index, row in new_data.iterrows():
        cursor.execute("INSERT INTO Ice_cds_open_interest (col1, col2, col3) VALUES (?, ?, ?)", 
                       (row['col1'], row['col2'], row['col3']))
    conn.commit()

# Function to find missing records and insert new data into the SQLite DB
def process_csv(file_path, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read CSV into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Get existing records from the database
    existing_data = pd.read_sql_query("SELECT col1, col2, col3 FROM Ice_cds_open_interest", conn)
    
    # Find records in the CSV that are not in the existing data
    merged_data = df.merge(existing_data, on=['col1', 'col2', 'col3'], how='left', indicator=True)
    new_records = merged_data[merged_data['_merge'] == 'left_only'].drop(columns=['_merge'])
    
    # Insert new records into the database
    if not new_records.empty:
        insert_new_data(new_records, cursor, conn)
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

# Create the database and table if it doesn't exist
create_db_if_not_exists(db_path)

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
