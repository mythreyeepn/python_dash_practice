import pandas as pd
import pyodbc

# === CONFIGURATION ===

csv_path = "data.csv"  # Path to your CSV file
sql_table = "YourTargetTable"  # Name of your SQL Server table

# Mapping of CSV columns to SQL Server columns
column_mapping = {
    "csv_col1": "sql_col1",
    "csv_col2": "sql_col2",
    "csv_col3": "sql_col3",
    "csv_col4": "sql_col4",
    "csv_col5": "sql_col5",
    "csv_col6": "sql_col6",
    "csv_col7": "sql_col7"
}

# SQL Server connection string (adjust as needed)
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=your_server_name;"
    "DATABASE=your_database_name;"
    "UID=your_username;"
    "PWD=your_password"
)

# === LOAD AND TRANSFORM CSV DATA ===

df = pd.read_csv(csv_path)

# Keep only the needed columns and rename them
df = df[list(column_mapping.keys())]
df.rename(columns=column_mapping, inplace=True)

# === INSERT INTO SQL SERVER ===

with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()

    # Prepare insert statement dynamically
    columns = ", ".join(df.columns)
    placeholders = ", ".join("?" for _ in df.columns)
    insert_sql = f"INSERT INTO {sql_table} ({columns}) VALUES ({placeholders})"

    for index, row in df.iterrows():
        cursor.execute(insert_sql, tuple(row))

    conn.commit()

print("Data inserted successfully.")
