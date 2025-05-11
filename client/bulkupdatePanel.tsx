
// AG Grid config with highlight handling
import { useRef, useEffect, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';

const SkewGrid = ({ rowData, currentUser }) => {
  const gridRef = useRef(null);

  const [columnDefs] = useState([
    {
      field: 'isin',
      headerName: 'ISIN'
    },
    {
      field: 'buy_skew',
      headerName: 'Buy Skew',
      editable: true,
      cellClassRules: {
        'cell-green': (params) => {
          const hs = params.data.highlightStatus?.[params.colDef.field];
          return hs?.color === 'green' && Date.now() < hs.expiresAt;
        },
        'cell-blue': (params) => {
          const hs = params.data.highlightStatus?.[params.colDef.field];
          return hs?.color === 'blue' && Date.now() < hs.expiresAt;
        }
      }
    },
    {
      field: 'sell_skew',
      headerName: 'Sell Skew',
      editable: true,
      cellClassRules: {
        'cell-green': (params) => {
          const hs = params.data.highlightStatus?.[params.colDef.field];
          return hs?.color === 'green' && Date.now() < hs.expiresAt;
        },
        'cell-blue': (params) => {
          const hs = params.data.highlightStatus?.[params.colDef.field];
          return hs?.color === 'blue' && Date.now() < hs.expiresAt;
        }
      }
    }
  ]);

  // Socket logic
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/trader-skews");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.event === "skew_updated") {
        const color = data.user_id === currentUser.id ? "green" : "blue";

        gridRef.current.api.applyTransaction({
          update: [{
            isin: data.isin,
            [data.column]: data.new_value,
            highlightStatus: {
              [data.column]: {
                color,
                expiresAt: Date.now() + 45000
              }
            }
          }]
        });
      }
    };

    return () => socket.close();
  }, [currentUser.id]);

  // Cleanup expired highlights every 10s
  useEffect(() => {
    const interval = setInterval(() => {
      if (!gridRef.current) return;
      gridRef.current.api.forEachNode((node) => {
        const highlight = node.data.highlightStatus;
        if (!highlight) return;
        let changed = false;

        for (const col in highlight) {
          if (Date.now() > highlight[col].expiresAt) {
            delete highlight[col];
            changed = true;
          }
        }

        if (changed) {
          gridRef.current.api.applyTransaction({ update: [node.data] });
        }
      });
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="ag-theme-alpine" style={{ height: 600 }}>
      <AgGridReact
        ref={gridRef}
        rowData={rowData}
        columnDefs={columnDefs}
        getRowId={params => params.data.isin}
      />
    </div>
  );
};

export default SkewGrid;


.cell-green {
  background-color: #d4edda !important;
  transition: background-color 0.3s ease;
}

.cell-blue {
  background-color: #cce5ff !important;
  transition: background-color 0.3s ease;
}