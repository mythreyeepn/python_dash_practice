import React, { useState } from 'react'
import { TextField, Button, Stack } from '@mui/material'
import { useBondStore } from '../store/bondStore'

const BulkUpdater = () => {
  const [buySkew, setBuySkew] = useState('')
  const [sellSkew, setSellSkew] = useState('')
  const [dnt, setDnt] = useState('')
  const { bulkUpdateVisible, bonds, selectedTrader } = useBondStore()

  const handleBulkUpdate = () => {
    const updates: any = {}
    if (buySkew) updates.buySkew = parseFloat(buySkew)
    if (sellSkew) updates.sellSkew = parseFloat(sellSkew)
    if (dnt) updates.dnt = dnt

    const filterFn = (bond: any) => bond.trader === selectedTrader
    bulkUpdateVisible(filterFn, updates)
  }

  return (
    <Stack direction="row" spacing={2} alignItems="center" mb={2}>
      <TextField label="Buy Skew" value={buySkew} onChange={e => setBuySkew(e.target.value)} />
      <TextField label="Sell Skew" value={sellSkew} onChange={e => setSellSkew(e.target.value)} />
      <TextField label="DNT" value={dnt} onChange={e => setDnt(e.target.value)} />
      <Button variant="contained" onClick={handleBulkUpdate}>Save</Button>
    </Stack>
  )
}

export default BulkUpdater
