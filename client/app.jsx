import React, { useEffect, useState } from 'react'
import {
  CssBaseline,
  Container,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  TextField,
  Grid,
  Typography,
  IconButton
} from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'
import { AgGridReact } from 'ag-grid-react'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-alpine.css'

const App = () => {
  const [bonds, setBonds] = useState([])
  const [traders, setTraders] = useState([])
  const [selectedTrader, setSelectedTrader] = useState('')
  const [buySkew, setBuySkew] = useState(0)
  const [sellSkew, setSellSkew] = useState(0)
  const [dnt, setDnt] = useState(0)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  useEffect(() => {
    const fetchMockData = async () => {
      const response = await fetch('/mockData.json')
      const data = await response.json()
      setTraders(data.traders)
      setBonds(data.bonds)
      if (data.traders.length > 0) {
        setSelectedTrader(data.traders[0].id)
      }
    }

    fetchMockData()
  }, [])

  const filteredBonds = bonds.filter(bond => bond.traderId === selectedTrader)

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

  const handleBulkUpdate = () => {
    const updatedBonds = bonds.map(bond => {
      if (bond.traderId === selectedTrader) {
        return {
          ...bond,
          buySkew,
          sellSkew,
          dnt,
        }
      }
      return bond
    })
    setBonds(updatedBonds)
  }

  const gridOptions = {
    defaultColDef: {
      sortable: true,
      filter: true,
      resizable: true,
    },
    rowData: filteredBonds,
  }

  const NavbarSidebar = ({ sidebarOpen, setSidebarOpen }) => {
    return (
      <Box sx={{ display: 'flex', height: '100vh' }}>
        <Box
          sx={{
            width: sidebarOpen ? '240px' : '60px',
            transition: 'width 0.3s',
            backgroundColor: '#2c3e50',
            color: '#fff',
            paddingTop: '20px',
            paddingLeft: '10px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
            height: '100vh',
          }}
        >
          <IconButton onClick={() => setSidebarOpen(!sidebarOpen)} sx={{ color: 'white' }}>
            <MenuIcon />
          </IconButton>
          {sidebarOpen && (
            <div style={{ marginTop: '20px' }}>
              <Typography variant="h6">Dashboard</Typography>
              <Typography variant="body1">Link 1</Typography>
              <Typography variant="body1">Link 2</Typography>
              <Typography variant="body1">Link 3</Typography>
            </div>
          )}
        </Box>

        <Box sx={{ flexGrow: 1, padding: '10px', backgroundColor: '#3f51b5', color: '#fff' }}>
          <Typography variant="h6">Bond Universe</Typography>
        </Box>
      </Box>
    )
  }

  return (
    <div>
      <CssBaseline />
      <NavbarSidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

      <Box sx={{ flexGrow: 1, padding: '20px' }}>
        <Container maxWidth="lg" sx={{ marginTop: '20px' }}>
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
  )
}

export default App
