import React, { useState } from 'react'
import {
  AppBar, Toolbar, IconButton, Typography,
  Drawer, List, ListItem, ListItemText
} from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'

const NavbarWithSidebar = () => {
  const [open, setOpen] = useState(false)

  return (
    <>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton edge="start" color="inherit" onClick={() => setOpen(true)}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6">Bond Universe</Typography>
        </Toolbar>
      </AppBar>

      <Drawer anchor="left" open={open} onClose={() => setOpen(false)}>
        <List>
          <ListItem button>
            <ListItemText primary="Dashboard" />
          </ListItem>
          <ListItem button>
            <ListItemText primary="Reports" />
          </ListItem>
        </List>
      </Drawer>
    </>
  )
}

export default NavbarWithSidebar
