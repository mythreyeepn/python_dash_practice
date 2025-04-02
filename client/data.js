import React, { useState, useEffect } from 'react';
import './App.css'; // For custom styles

const SDRTable = () => {
  const [trades, setTrades] = useState([]); // To store trades

  useEffect(() => {
    // WebSocket setup for receiving data from FastAPI
    const ws = new WebSocket('ws://localhost:8000/ws/sdr'); // Adjust with your FastAPI URL
    ws.onmessage = (event) => {
      const newTrades = JSON.parse(event.data);
      // Add new trades at the top of the list
      setTrades((prevTrades) => [...newTrades, ...prevTrades]);
    };

    return () => {
      // Clean up WebSocket connection on unmount
      if (ws) {
        ws.close();
      }
    };
  }, []);

  return (
    <div>
      {/* Navbar */}
      <nav className="navbar">
        <h2>SDR Trade Dashboard</h2>
      </nav>

      {/* SDR Table */}
      <h3>Real-Time SDR Trades</h3>
      <table className="sdr-table">
        <thead>
          <tr>
            <th>Dissemination ID</th>
            <th>Execution Timestamp</th>
            <th>Other Columns</th> {/* Adjust with your trade columns */}
          </tr>
        </thead>
        <tbody>
          {trades.map((trade, index) => (
            <tr key={trade.disseminationId} className={index % 2 === 0 ? 'even' : 'odd'}>
              <td>{trade.disseminationId}</td>
              <td>{trade.executionTimestamp}</td>
              <td>{trade.otherColumn}</td> {/* Adjust with your trade data */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SDRTable;
