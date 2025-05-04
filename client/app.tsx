import React, { useEffect } from 'react';
import { CssBaseline, Box, AppBar, Toolbar, Typography, IconButton, Drawer, List, ListItem, ListItemText, Divider } from '@mui/material';
import { Menu } from '@mui/icons-material';
import { useBondStore } from './store';
import BondsGrid from './BondsGrid';
import BulkUpdatePanel from './BulkUpdatePanel';
import TraderDropdown from './TraderDropdown';

const App = () => {
  const { traders, setTraders, setSelectedTrader, selectedTrader } = useBondStore();

  // Mock data for traders and bonds
  useEffect(() => {
    const mockTraders = [
      { id: '1', name: 'Trader A' },
      { id: '2', name: 'Trader B' },
      { id: '3', name: 'Trader C' },
    ];
    setTraders(mockTraders);
    setSelectedTrader(mockTraders[0]); // Default trader selection
  }, [setTraders, setSelectedTrader]);

  return (
    <>
      <CssBaseline />
      <AppBar position="sticky">
        <Toolbar>
          <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
            <Menu />
          </IconButton>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Bond Universe
          </Typography>
        </Toolbar>
      </AppBar>
      <Box sx={{ display: 'flex' }}>
        {/* Side Navigation */}
        <Drawer
          sx={{
            width: 240,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: 240,
              boxSizing: 'border-box',
            },
          }}
          variant="permanent"
          anchor="left"
        >
          <List>
            <ListItem>
              <TraderDropdown />
            </ListItem>
            <Divider />
            <ListItem button>
              <ListItemText primary="Other Option 1" />
            </ListItem>
            <ListItem button>
              <ListItemText primary="Other Option 2" />
            </ListItem>
          </List>
        </Drawer>

        {/* Main Content */}
        <Box component="main" sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}>
          <BondsGrid />
          <BulkUpdatePanel />
        </Box>
      </Box>
    </>
  );
};

export default App;


// src/App.tsx
import React, { useEffect } from 'react';
import { useBondStore } from './store/bondStore';
import TraderDropdown from './components/TraderDropdown';
import BulkUpdatePanel from './components/BulkUpdatePanel';
import BondsGrid from './components/BondsGrid';

const App = () => {
  const { setAllBonds } = useBondStore();

  // Fetching the bond data from the backend
  useEffect(() => {
    // Simulated backend call, replace with your actual backend API
    const fetchBonds = async () => {
      const response = await fetch('/api/bonds');
      const bonds = await response.json();
      setAllBonds(bonds);
    };

    fetchBonds();
  }, [setAllBonds]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Bond Universe</h1>
      <TraderDropdown />
      <BulkUpdatePanel />
      <BondsGrid />
    </div>
  );
};

export default App;
