import React, { useEffect, useState } from 'react'
import { CssBaseline, Container, Box, Typography, FormControl, InputLabel, Select, MenuItem, Button, TextField, Grid } from '@mui/material'
import { useBondStore } from './store/bondStore'
import { AgGridReact } from 'ag-grid-react'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-alpine.css'

const App = () => {
  const { setBonds, setTraders, bonds, traders } = useBondStore()

  const [selectedTrader, setSelectedTrader] = useState<string>(traders[0]?.id || '')
  const [buySkew, setBuySkew] = useState<number>(0)
  const [sellSkew, setSellSkew] = useState<number>(0)
  const [dnt, setDnt] = useState<number>(0)

  // Fetch mock data and set it to store on page load
  useEffect(() => {
    const fetchMockData = async () => {
      const response = await fetch('/mockData.json')
      const data = await response.json()
      setTraders(data.traders)
      setBonds(data.bonds)
    }

    fetchMockData()
  }, [setBonds, setTraders])

  // Filter bonds based on selected trader
  const filteredBonds = bonds.filter(bond => bond.traderId === selectedTrader)

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
  ]

  // Handle changes for Buy/Sell Skew and DNT
  const handleBulkUpdate = () => {
    const updatedBonds = filteredBonds.map(bond => ({
      ...bond,
      buySkew,
      sellSkew,
      dnt,
    }))
    setBonds([
      ...bonds.filter(bond => bond.traderId !== selectedTrader), 
      ...updatedBonds,
    ])
  }

  // AG Grid options
  const gridOptions = {
    defaultColDef: {
      sortable: true,
      filter: true,
      resizable: true,
    },
    rowData: filteredBonds,
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <CssBaseline />

      {/* Navbar and Sidebar */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#3f51b5', color: '#fff', padding: '10px' }}>
        <Typography variant="h6">Bond Universe</Typography>
      </Box>

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
    </div>
  )
}

export default App
