import React, { useEffect } from 'react'
import { CssBaseline, Container, Box, Typography } from '@mui/material'
import { useBondStore } from './store/bondStore'
import NavbarWithSidebar from './components/NavbarWithSidebar'
import TraderSelector from './components/TraderSelector'
import BulkUpdater from './components/BulkUpdater'
import BondTable from './components/BondTable'

const App = () => {
  const { setBonds, setTraders } = useBondStore()

  // Fetch mock data and set it to store on page load
  useEffect(() => {
    const fetchMockData = async () => {
      const response = await fetch('/mockData.json')
      const data = await response.json()
      setTraders(data.traders)  // Set traders to Zustand store
      setBonds(data.bonds)  // Set bonds to Zustand store
    }

    fetchMockData()
  }, [setBonds, setTraders])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      {/* Navbar and Sidebar */}
      <NavbarWithSidebar />

      <Box sx={{ flexGrow: 1, mt: 8, px: 3 }}>
        {/* Main content */}
        <Container maxWidth="lg">
          <Typography variant="h4" gutterBottom>
            Bond Universe
          </Typography>

          {/* Trader Selector */}
          <TraderSelector />

          {/* Bulk Update Section */}
          <BulkUpdater />

          {/* Bond Table */}
          <BondTable />
        </Container>
      </Box>
    </div>
  )
}

export default App
