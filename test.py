import sqlite3
from dash import Dash, dcc, html, Input, Output, State, dash_table

# Initialize the app
app = Dash(__name__)

# Create SQLite connection and ensure table exists with is_deleted column for each type
def create_db():
    conn = sqlite3.connect('mapping.db')
    c = conn.cursor()
    # Create tables for ticker_mapping, time_mapping, and data_mapping
    c.execute('''CREATE TABLE IF NOT EXISTS ticker_mapping
                 (s_no INTEGER PRIMARY KEY, ticker TEXT, id_mapping TEXT, is_deleted BOOLEAN DEFAULT FALSE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS time_mapping
                 (s_no INTEGER PRIMARY KEY, time TEXT, description TEXT, is_deleted BOOLEAN DEFAULT FALSE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS data_mapping
                 (s_no INTEGER PRIMARY KEY, data_key TEXT, data_value TEXT, is_deleted BOOLEAN DEFAULT FALSE)''')
    conn.commit()
    conn.close()

create_db()

# App layout with Tabs
app.layout = html.Div([
    html.H1("Mappings"),

    # Tabs for different mappings
    dcc.Tabs([
        dcc.Tab(label='Ticker Mapping', children=[
            # DataTable for Ticker Mapping
            dash_table.DataTable(
                id='ticker-editable-table',
                columns=[
                    {"name": "S.No", "id": "s.no", "type": "numeric", "hideable": True},
                    {"name": "Ticker", "id": "ticker", "type": "text"},
                    {"name": "ID Mapping", "id": "id_mapping", "type": "text"},
                ],
                data=[],  # Initially empty data for ticker mapping
                editable=True,
                row_deletable=True,
                sort_action="native",
                filter_action="native",
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'fontSize': '14px',
                },
                style_header={
                    'backgroundColor': 'lightgrey',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                },
                selected_rows=[],
            ),
            # Inputs for adding ticker rows
            html.Div([
                dcc.Input(id="input-ticker", type="text", placeholder="Ticker"),
                dcc.Input(id="input-idmapping", type="text", placeholder="ID Mapping"),
                html.Button("Add Row", id="add-ticker-btn", n_clicks=0),
            ], style={"marginTop": 20, "textAlign": "center"}),
        ]),

        dcc.Tab(label='Time Mapping', children=[
            # DataTable for Time Mapping
            dash_table.DataTable(
                id='time-editable-table',
                columns=[
                    {"name": "S.No", "id": "s.no", "type": "numeric", "hideable": True},
                    {"name": "Time", "id": "time", "type": "text"},
                    {"name": "Description", "id": "description", "type": "text"},
                ],
                data=[],  # Initially empty data for time mapping
                editable=True,
                row_deletable=True,
                sort_action="native",
                filter_action="native",
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'fontSize': '14px',
                },
                style_header={
                    'backgroundColor': 'lightgrey',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                },
                selected_rows=[],
            ),
            # Inputs for adding time rows
            html.Div([
                dcc.Input(id="input-time", type="text", placeholder="Time"),
                dcc.Input(id="input-description", type="text", placeholder="Description"),
                html.Button("Add Row", id="add-time-btn", n_clicks=0),
            ], style={"marginTop": 20, "textAlign": "center"}),
        ]),

        dcc.Tab(label='Data Mapping', children=[
            # DataTable for Data Mapping
            dash_table.DataTable(
                id='data-editable-table',
                columns=[
                    {"name": "S.No", "id": "s.no", "type": "numeric", "hideable": True},
                    {"name": "Data Key", "id": "data_key", "type": "text"},
                    {"name": "Data Value", "id": "data_value", "type": "text"},
                ],
                data=[],  # Initially empty data for data mapping
                editable=True,
                row_deletable=True,
                sort_action="native",
                filter_action="native",
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'fontSize': '14px',
                },
                style_header={
                    'backgroundColor': 'lightgrey',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                },
                selected_rows=[],
            ),
            # Inputs for adding data rows
            html.Div([
                dcc.Input(id="input-data_key", type="text", placeholder="Data Key"),
                dcc.Input(id="input-data_value", type="text", placeholder="Data Value"),
                html.Button("Add Row", id="add-data-btn", n_clicks=0),
            ], style={"marginTop": 20, "textAlign": "center"}),
        ]),

    ])
])

# Combined callback for adding rows to respective tables
@app.callback(
    [Output('ticker-editable-table', 'data'),
     Output('time-editable-table', 'data'),
     Output('data-editable-table', 'data'),
     Output('input-ticker', 'value'),
     Output('input-idmapping', 'value'),
     Output('input-time', 'value'),
     Output('input-description', 'value'),
     Output('input-data_key', 'value'),
     Output('input-data_value', 'value')],
    [Input('add-ticker-btn', 'n_clicks'),
     Input('add-time-btn', 'n_clicks'),
     Input('add-data-btn', 'n_clicks')],
    [State('input-ticker', 'value'),
     State('input-idmapping', 'value'),
     State('input-time', 'value'),
     State('input-description', 'value'),
     State('input-data_key', 'value'),
     State('input-data_value', 'value'),
     State('ticker-editable-table', 'data'),
     State('time-editable-table', 'data'),
     State('data-editable-table', 'data')]
)
def update_table(ticker_clicks, time_clicks, data_clicks, ticker, id_mapping, time, description, data_key, data_value, ticker_data, time_data, data_data):
    # Initialize updated data lists for each table
    updated_ticker_data = ticker_data or []
    updated_time_data = time_data or []
    updated_data_data = data_data or []

    # Add new ticker row if button clicked
    if ticker_clicks > 0 and ticker and id_mapping:
        # Add to SQLite database
        conn = sqlite3.connect('mapping.db')
        c = conn.cursor()
        c.execute("INSERT INTO ticker_mapping (ticker, id_mapping, is_deleted) VALUES (?, ?, ?)", (ticker, id_mapping, False))
        conn.commit()
        conn.close()
        
        # Add to DataTable
        updated_ticker_data.append({"s.no": len(updated_ticker_data) + 1, "ticker": ticker, "id_mapping": id_mapping, "is_deleted": False})

    # Add new time row if button clicked
    if time_clicks > 0 and time and description:
        # Add to SQLite database
        conn = sqlite3.connect('mapping.db')
        c = conn.cursor()
        c.execute("INSERT INTO time_mapping (time, description, is_deleted) VALUES (?, ?, ?)", (time, description, False))
        conn.commit()
        conn.close()
        
        # Add to DataTable
        updated_time_data.append({"s.no": len(updated_time_data) + 1, "time": time, "description": description, "is_deleted": False})

    # Add new data row if button clicked
    if data_clicks > 0 and data_key and data_value:
        # Add to SQLite database
        conn = sqlite3.connect('mapping.db')
        c = conn.cursor()
        c.execute("INSERT INTO data_mapping (data_key, data_value, is_deleted) VALUES (?, ?, ?)", (data_key, data_value, False))
        conn.commit()
        conn.close()

        # Add to DataTable
        updated_data_data.append({"s.no": len(updated_data_data) + 1, "data_key": data_key, "data_value": data_value, "is_deleted": False})

    # Clear input fields after adding a row
    return updated_ticker_data, updated_time_data, updated_data_data, "", "", "", "", "", ""

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
