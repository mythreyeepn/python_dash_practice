from dash import Dash, dcc, html, Input, Output, State, dash_table
import json

# Initialize the app
app = Dash(__name__)

# Initial dummy data
dummy_data = [
    {"s.no": 1, "ticker": "AAPL", "id_mapping": "12345"},
    {"s.no": 2, "ticker": "GOOG", "id_mapping": "67890"},
    {"s.no": 3, "ticker": "MSFT", "id_mapping": "11111"},
    {"s.no": 4, "ticker": "AA", "id_mapping": "22222"},
]

# App layout
app.layout = html.Div([
    html.H1("Auto-Incremented S.No Table"),

    # DataTable with filters in header rows
    dash_table.DataTable(
        id='editable-table',
        columns=[
            {"name": "S.No", "id": "s.no", "type": "numeric"},
            {"name": "Ticker", "id": "ticker", "type": "text"},
            {"name": "ID Mapping", "id": "id_mapping", "type": "text"},
        ],
        data=dummy_data,
        editable=True,
        row_deletable=True,
        sort_action="native",
        filter_action="native",  # Enables native column-level filtering
        style_table={'overflowX': 'auto'},
        merge_duplicate_headers=True,  # Merge header rows
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
    ),

    # Inputs for adding rows
    html.Div([
        dcc.Input(id="input-ticker", type="text", placeholder="Ticker"),
        dcc.Input(id="input-idmapping", type="text", placeholder="ID Mapping"),
        html.Button("Add Row", id="add-row-btn", n_clicks=0),
    ], style={"marginTop": 20, "textAlign": "center"}),

    # Save button
    html.Button("Save to JSON", id="save-btn", n_clicks=0, style={"marginTop": 20}),
    html.Div(id="save-confirmation", style={"marginTop": 10, "textAlign": "center"}),
])

# Callbacks

@app.callback(
    Output('editable-table', 'data'),
    Input('add-row-btn', 'n_clicks'),
    Input('editable-table', 'data'),
    State('input-ticker', 'value'),
    State('input-idmapping', 'value'),
)
def update_table(add_clicks, rows, ticker, id_mapping):
    # Ensure we have a working copy of rows
    updated_rows = rows or []

    # Add a new row if add button clicked
    if add_clicks > 0 and ticker and id_mapping:
        updated_rows.append({"s.no": len(updated_rows) + 1, "ticker": ticker, "id_mapping": id_mapping})

    # Recalculate `S.No` for all rows (auto-adjust after delete or filter)
    for index, row in enumerate(updated_rows):
        row['s.no'] = index + 1

    return updated_rows

@app.callback(
    Output('save-confirmation', 'children'),
    Input('save-btn', 'n_clicks'),
    State('editable-table', 'data'),
)
def save_to_json(n_clicks, rows):
    if n_clicks > 0:
        with open("table_data.json", "w") as f:
            json.dump(rows, f, indent=4)
        return "Data saved to table_data.json!"
    return ""

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
