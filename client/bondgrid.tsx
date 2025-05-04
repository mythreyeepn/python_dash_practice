import React, { useMemo, useCallback } from 'react'
import { AgGridReact } from 'ag-grid-react'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-alpine.css'
import { useBondStore } from '../store/bondStore'
import debounce from 'lodash.debounce'

const BondTable = () => {
  const { bonds, selectedTrader, updateBond } = useBondStore()

  const rowData = useMemo(() => bonds.filter(b => b.trader === selectedTrader), [bonds, selectedTrader])

  const onCellValueChanged = useCallback(
    debounce((event: any) => {
      const { data } = event
      updateBond(data.isin, {
        buySkew: data.buySkew,
        sellSkew: data.sellSkew,
        dnt: data.dnt,
      })
    }, 1000),
    []
  )

  const columnDefs = useMemo(() => [
    { field: 'sector', sortable: true, filter: true },
    { field: 'maturity', sortable: true, filter: true },
    { field: 'rating', sortable: true, filter: true },
    { field: 'ticker', sortable: true, filter: true },
    { field: 'isin', sortable: true, filter: true },
    { field: 'buySkew', editable: true, sortable: true, filter: true },
    { field: 'sellSkew', editable: true, sortable: true, filter: true },
    { field: 'dnt', editable: true, sortable: true, filter: true },
  ], [])

  return (
    <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}>
      <AgGridReact
        rowData={rowData}
        columnDefs={columnDefs}
        onCellValueChanged={onCellValueChanged}
        pagination={true}
        paginationPageSize={100}
      />
    </div>
  )
}

export default BondTable
