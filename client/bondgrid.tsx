import React, { useEffect } from 'react';
import { DataGrid, GridColDef, GridRowsProp } from '@mui/x-data-grid';
import { useBondStore } from './store';

const BondsGrid = () => {
  const { selectedTrader, bonds, setBonds } = useBondStore();

  useEffect(() => {
    // Fetch bonds data from the backend (mocked here for now)
    const mockBonds = [
      { sector: 'Tech', maturity: '2025-12-01', rating: 'AAA', ticker: 'AAPL', isin: 'US0378331005', buySkew: '0.01', sellSkew: '0.02', dnt: 'N' },
      { sector: 'Tech', maturity: '2026-05-01', rating: 'AA', ticker: 'GOOG', isin: 'US02079K3059', buySkew: '0.02', sellSkew: '0.03', dnt: 'Y' },
      { sector: 'Finance', maturity: '2027-11-01', rating: 'BBB', ticker: 'MSFT', isin: 'US5949181045', buySkew: '0.03', sellSkew: '0.04', dnt: 'N' },
    ];
    setBonds(mockBonds); // Set the bond data for now
  }, [setBonds]);

  const columns: GridColDef[] = [
    { field: 'sector', headerName: 'Sector', width: 150 },
    { field: 'maturity', headerName: 'Maturity', width: 150 },
    { field: 'rating', headerName: 'Rating', width: 150 },
    { field: 'ticker', headerName: 'Ticker', width: 150 },
    { field: 'isin', headerName: 'ISIN', width: 180 },
    { field: 'buySkew', headerName: 'Buy Skew', editable: true, width: 150 },
    { field: 'sellSkew', headerName: 'Sell Skew', editable: true, width: 150 },
    { field: 'dnt', headerName: 'DNT', editable: true, width: 100 },
  ];

  const rows: GridRowsProp = bonds.map((bond, index) => ({
    id: index + 1,
    sector: bond.sector,
    maturity: bond.maturity,
    rating: bond.rating,
    ticker: bond.ticker,
    isin: bond.isin,
    buySkew: bond.buySkew,
    sellSkew: bond.sellSkew,
    dnt: bond.dnt,
  }));

  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid rows={rows} columns={columns} pageSize={5} />
    </div>
  );
};

export default BondsGrid;



// src/components/BondsGrid.tsx
import React from 'react';
import { useBondStore } from '../store/bondStore';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-react/styles/ag-grid.css';
import 'ag-grid-react/styles/ag-theme-alpine.css';

const BondsGrid = () => {
  const { filteredBonds, updateBond } = useBondStore();

  const columnDefs = [
    { headerName: "Sector", field: "sector", sortable: true, filter: true },
    { headerName: "Maturity", field: "maturity", sortable: true, filter: true },
    { headerName: "Rating", field: "rating", sortable: true, filter: true },
    { headerName: "Ticker", field: "ticker", sortable: true, filter: true },
    { headerName: "ISIN", field: "isin", sortable: true, filter: true },
    {
      headerName: "Buy Skew", 
      field: "buySkew", 
      editable: true,
      valueSetter: (params: any) => {
        const value = params.newValue;
        updateBond(params.data.isin, { buySkew: value });
        return true;
      }
    },
    {
      headerName: "Sell Skew", 
      field: "sellSkew", 
      editable: true,
      valueSetter: (params: any) => {
        const value = params.newValue;
        updateBond(params.data.isin, { sellSkew: value });
        return true;
      }
    },
    {
      headerName: "DNT", 
      field: "dnt", 
      editable: true,
      valueSetter: (params: any) => {
        const value = params.newValue;
        updateBond(params.data.isin, { dnt: value });
        return true;
      }
    }
  ];

  const gridOptions = {
    pagination: true,
    rowSelection: 'multiple',
  };

  return (
    <div className="ag-theme-alpine" style={{ height: '500px', width: '100%' }}>
      <AgGridReact
        columnDefs={columnDefs}
        rowData={filteredBonds}
        gridOptions={gridOptions}
        domLayout='autoHeight'
      />
    </div>
  );
};

export default BondsGrid;

