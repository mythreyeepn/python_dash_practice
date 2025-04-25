// TradeInputPage.tsx
import React, { useEffect, useRef, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './TradeInputPage.css';

const TradeInputPage = () => {
  const [rowData, setRowData] = useState([]);
  const gridRef = useRef(null);

  const columnDefs = [
    { field: 'id', editable: false },
    { field: 'factor', editable: true },
    { field: 'weight', editable: true },
    { field: 'lastModified', editable: false },
  ];

  useEffect(() => {
    fetch('/data')
      .then((res) => res.json())
      .then((data) => setRowData(data));
  }, []);

  return (
    <div className="page-container">
      <nav className="navbar">Trade Input</nav>
      <div className="grid-container ag-theme-alpine">
        <AgGridReact
          ref={gridRef}
          rowData={rowData}
          columnDefs={columnDefs}
          defaultColDef={{ sortable: true, filter: true, resizable: true }}
          rowClassRules={{
            'row-even': 'function(params) { return params.node.rowIndex % 2 === 0 }',
            'row-odd': 'function(params) { return params.node.rowIndex % 2 === 1 }',
          }}
          domLayout="autoHeight"
          suppressRowClickSelection
          editType="fullRow"
        />
      </div>
    </div>
  );
};

export default TradeInputPage;
