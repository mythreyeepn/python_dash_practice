// App.jsx

import React, { useEffect, useState } from 'react';
import { CssBaseline, Container, Box, FormControl, InputLabel, Select, MenuItem, Button, TextField, Grid } from '@mui/material';
import { useBondStore } from './store/bondStore';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import NavbarSidebar from './components/NavbarSidebar';  // Import NavbarSidebar

const App = () => {
  const { setBonds, setTraders, bonds, traders } = useBondStore();

  const [selectedTrader, setSelectedTrader] = useState(traders[0]?.id || '');
  const [buySkew, setBuySkew] = useState(0);
  const [sellSkew, setSellSkew] = useState(0);
  const [dnt, setDnt] = useState(0);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Fetch mock data and set it to store on page load
  useEffect(() => {
    const fetchMockData = async () => {
      const response = await fetch('/mockData.json');
      const data = await response.json();
      setTraders(data.traders);
      setBonds(data.bonds);
    };

    fetchMockData();
  }, [setBonds, setTraders]);

  // Filter bonds based on selected trader
  const filteredBonds = bonds.filter(bond => bond.traderId === selectedTrader);

  // Columns for AG Grid
  const columns = [
    { headerName: 'Sector', field: 'sector' },
    { headerName: 'Maturity', field: 'maturity' },
    { headerName: 'Rating', field: 'rating' },
    { headerName: 'Ticker', field: 'ticker' },
    { headerName: 'ISIN', field: 'isin' },
    {
      headerName: 'Buy Skew',
      field: 'buySkew',
      editable: true,
      cellEditor: 'agTextCellEditor',
    },
    {
      headerName: 'Sell Skew',
      field: 'sellSkew',
      editable: true,
      cellEditor: 'agTextCellEditor',
    },
    {
      headerName: 'DNT',
      field: 'dnt',
      editable: true,
      cellEditor: 'agTextCellEditor',
    },
  ];

  // Handle changes for Buy/Sell Skew and DNT
  const handleBulkUpdate = () => {
    const updatedBonds = filteredBonds.map(bond => ({
      ...bond,
      buySkew,
      sellSkew,
      dnt,
    }));
    setBonds([
      ...bonds.filter(bond => bond.traderId !== selectedTrader),
      ...updatedBonds,
    ]);
  };

  // AG Grid options
  const gridOptions = {
    defaultColDef: {
      sortable: true,
      filter: true,
      resizable: true,
    },
    rowData: filteredBonds,
  };

  return (
    <div>
      <CssBaseline />

      {/* Navbar and Sidebar Component */}
      <NavbarSidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      {/* Main Content */}
      <Box sx={{ flexGrow: 1, padding: '20px' }}>
        <Container maxWidth="lg" sx={{ marginTop: '20px' }}>
          {/* Trader Dropdown */}
          <FormControl fullWidth sx={{ marginBottom: '20px' }}>
            <InputLabel>Trader</InputLabel>
            <Select
              value={selectedTrader}
              label="Trader"
              onChange={(e) => setSelectedTrader(e.target.value)}
            >
              {traders.map(trader => (
                <MenuItem key={trader.id} value={trader.id}>
                  {trader.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Bulk Update Section */}
          <Grid container spacing={2} sx={{ marginBottom: '20px' }}>
            <Grid item xs={4}>
              <TextField
                label="Buy Skew"
                type="number"
                fullWidth
                value={buySkew}
                onChange={(e) => setBuySkew(parseFloat(e.target.value))}
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                label="Sell Skew"
                type="number"
                fullWidth
                value={sellSkew}
                onChange={(e) => setSellSkew(parseFloat(e.target.value))}
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                label="DNT"
                type="number"
                fullWidth
                value={dnt}
                onChange={(e) => setDnt(parseFloat(e.target.value))}
              />
            </Grid>
          </Grid>
          <Button variant="contained" color="primary" onClick={handleBulkUpdate}>
            Bulk Update
          </Button>

          {/* AG Grid */}
          <div className="ag-theme-alpine" style={{ height: '600px', marginTop: '20px' }}>
            <AgGridReact
              columnDefs={columns}
              gridOptions={gridOptions}
              defaultColDef={{ sortable: true, filter: true, editable: true }}
              domLayout="autoHeight"
            />
          </div>
        </Container>
      </Box>
    </div>
  );
};

export default App;
