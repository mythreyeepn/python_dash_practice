import React from 'react';
import { MenuItem, Select, InputLabel, FormControl } from '@mui/material';
import { useBondStore } from './store';

const TraderDropdown = () => {
  const { traders, selectedTrader, setSelectedTrader } = useBondStore();

  return (
    <FormControl fullWidth>
      <InputLabel id="trader-select-label">Select Trader</InputLabel>
      <Select
        labelId="trader-select-label"
        value={selectedTrader?.id || ''}
        label="Select Trader"
        onChange={(e) => {
          const selected = traders.find((trader) => trader.id === e.target.value);
          setSelectedTrader(selected);
        }}
      >
        {traders.map((trader) => (
          <MenuItem key={trader.id} value={trader.id}>
            {trader.name}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default TraderDropdown;
