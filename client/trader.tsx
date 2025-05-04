import React from 'react'
import { useBondStore } from '../store/bondStore'
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material'

const TraderSelector = () => {
  const { bonds, selectedTrader, setSelectedTrader } = useBondStore()
  const traders = Array.from(new Set(bonds.map(b => b.trader)))

  return (
    <FormControl fullWidth margin="normal">
      <InputLabel>Trader</InputLabel>
      <Select
        value={selectedTrader}
        onChange={e => setSelectedTrader(e.target.value)}
        label="Trader"
      >
        {traders.map(trader => (
          <MenuItem key={trader} value={trader}>{trader}</MenuItem>
        ))}
      </Select>
    </FormControl>
  )
}

export default TraderSelector
