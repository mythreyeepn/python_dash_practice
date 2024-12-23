import sqlite3
import pandas as pd

# File and table details
excel_file = 'data.xlsx'  # Replace with your file path
sheet_name = 'Sheet1'  # Replace with your sheet name
db_file = 'your_database.db'  # SQLite database file
table_name = 'your_table'  # Target database table name

# Read Excel file into a pandas DataFrame
data = pd.read_excel(excel_file, sheet_name=sheet_name)

# Select specific columns to insert (replace 'Column1' and 'Column2' with actual column names in Excel)
data_to_insert = data[['Column1', 'Column2']]  # Adjust to match your column names

# Connect to SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create table if it doesn't exist (adjust column types as necessary)
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    column1 TEXT,
    column2 TEXT,
    column3 TEXT DEFAULT NULL,
    column4 TEXT DEFAULT NULL
);
""")

# Insert data into the table
data_to_insert = data_to_insert.values.tolist()  # Convert DataFrame to list of tuples
cursor.executemany(f"INSERT INTO {table_name} (column1, column2) VALUES (?, ?)", data_to_insert)

# Commit changes and close connection
conn.commit()
conn.close()

print("Data inserted successfully!")
