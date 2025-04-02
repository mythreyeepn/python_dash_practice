import pytz
from datetime import datetime
import qpython.qconnection as qconn
from collections import deque

# Define EST timezone
EST = pytz.timezone('US/Eastern')

# In-memory storage for SDR trades
sdr_trades = deque(maxlen=1000)  # Stores latest trades (adjust size as needed)
seen_trade_ids = set()  # Track seen trades to avoid duplicates
latest_timestamp = None  # Track the last trade timestamp

# Function to fetch new trades from kdb
def fetch_new_trades():
    global latest_timestamp
    with qconn.QConnection(host='your_kdb_host', port=your_kdb_port, username='user', password='pass') as q:
        query = f"select from trades where executionTimestamp >= {latest_timestamp}" if latest_timestamp else "select from trades"
        result = q(query)
        if result:
            new_trades = [trade for trade in result if trade['disseminationId'] not in seen_trade_ids]
            for trade in new_trades:
                seen_trade_ids.add(trade['disseminationId'])
            
            if new_trades:
                latest_timestamp = max(trade['executionTimestamp'] for trade in new_trades)  # Update last timestamp

                # Convert executionTimestamp from UTC to EST before sending to UI
                for trade in new_trades:
                    # Assuming executionTimestamp is in UTC
                    execution_time_utc = trade['executionTimestamp']
                    
                    # If the timestamp is a string, first convert to datetime object
                    if isinstance(execution_time_utc, str):
                        execution_time_utc = datetime.strptime(execution_time_utc, "%Y-%m-%dT%H:%M:%S.%fZ")  # Example UTC format
                    
                    # Convert from UTC to EST
                    execution_time_est = execution_time_utc.astimezone(EST)

                    # Update the trade with the converted EST time for UI display
                    trade['executionTimestamp'] = execution_time_est.strftime("%Y-%m-%d %H:%M:%S")

                sdr_trades.extend(new_trades)
            return new_trades
        return []
