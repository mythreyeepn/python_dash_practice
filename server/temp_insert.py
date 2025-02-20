from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# SQL Server Configuration
server = 'your-server-name'
database = 'your-db-name'
driver = '{ODBC Driver 17 for SQL Server}'  # Ensure this driver is installed on your system

# Connection string
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    rfqId = data.get('rfqId')
    summaryStrings = data.get('summaryStrings')

    if not rfqId or not isinstance(summaryStrings, list) or len(summaryStrings) == 0:
        return jsonify({'message': 'Missing rfqId or summaryStrings'}), 400

    try:
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                for summaryString in summaryStrings:
                    cursor.execute(
                        "INSERT INTO your_table (rfq_id, summary_string) VALUES (?, ?)",
                        (rfqId, summaryString)
                    )
                conn.commit()

        return jsonify({'message': 'Data inserted successfully'}), 201
    except Exception as e:
        print("SQL Server error:", e)
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/summary/<int:ptId>', methods=['GET'])
def get_summary(ptId):
    """Fetches summaryStrings for a given ptId."""
    try:
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                query = "SELECT summary_string FROM your_table WHERE rfq_id = ?"
                cursor.execute(query, (ptId,))
                results = cursor.fetchall()

        # If results exist, return them as a list
        if results:
            summaries = [row[0] for row in results]
            return jsonify({'ptId': ptId, 'summaryStrings': summaries}), 200
        else:
            return jsonify({'message': 'No data found for given ptId'}), 404

    except Exception as e:
        print("SQL Server error:", e)
        return jsonify({'message': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(port=3000)
