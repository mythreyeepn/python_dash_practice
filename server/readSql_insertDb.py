import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# File paths
csv_file_path = "ydrive/repo/downloads/data.csv"
sqlite_db_path = "ydrive/repo/data/db/database.db"

def insert_csv_to_sqlite(csv_file, db_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Add ref_date and ref_hour columns
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    ref_hour = "05:00"
    data['ref_date'] = yesterday
    data['ref_hour'] = ref_hour

    # Replace empty values with None (NULL in SQLite)
    data = data.where(pd.notnull(data), None)

    # Connect to the SQLite database
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table statement
    columns = [f"{col} TEXT" for col in data.columns[:-2]] + ["ref_date TEXT", "ref_hour TEXT"]
    table_name = "data_table"
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
    cursor.execute(create_table_query)

    # Insert data into the table
    insert_query = f"INSERT INTO {table_name} ({', '.join(data.columns)}) VALUES ({', '.join(['?' for _ in data.columns])});"
    cursor.executemany(insert_query, data.values.tolist())

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Data inserted successfully into {db_file}")

def main():
    insert_csv_to_sqlite(csv_file_path, sqlite_db_path)

if __name__ == "__main__":
    main()
