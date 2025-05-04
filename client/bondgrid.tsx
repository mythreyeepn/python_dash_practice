// components/NavbarSidebar.tsx

import React from 'react'
import { Box, Typography, IconButton } from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'

interface NavbarSidebarProps {
  sidebarOpen: boolean
  setSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>
}

const NavbarSidebar: React.FC<NavbarSidebarProps> = ({ sidebarOpen, setSidebarOpen }) => {
  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      {/* Sidebar */}
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
            {/* Add links here */}
            <Typography variant="body1">Link 1</Typography>
            <Typography variant="body1">Link 2</Typography>
            <Typography variant="body1">Link 3</Typography>
          </div>
        )}
      </Box>

      {/* Navbar */}
      <Box sx={{ flexGrow: 1, padding: '10px', backgroundColor: '#3f51b5', color: '#fff' }}>
        <Typography variant="h6">Bond Universe</Typography>
      </Box>
    </Box>
  )
}

export default NavbarSidebar
