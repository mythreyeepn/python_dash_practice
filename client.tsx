import React, { useState } from 'react';
import './TradeDashboard.css';

const TradeDashboard: React.FC = () => {
  const [selectedTicker, setSelectedTicker] = useState<string | null>(null);

  const trades = [
    { id: 1, ticker: 'AAPL', price: 150, quantity: 100 },
    { id: 2, ticker: 'GOOGL', price: 2800, quantity: 50 },
    { id: 3, ticker: 'MSFT', price: 330, quantity: 75 },
  ];

  const childData = {
    AAPL: { details: 'Apple trade details' },
    GOOGL: { details: 'Google trade details' },
    MSFT: { details: 'Microsoft trade details' },
  };

  return (
    <div className="dashboard">
      {/* Top Section */}
      <div className="top-section">
        <div className="ticker-display">
          {selectedTicker ? `Selected Ticker: ${selectedTicker}` : 'Select a Ticker'}
        </div>
        <div className="toggle-buttons">
          <button>Toggle 1</button>
          <button>Toggle 2</button>
          <button>Toggle 3</button>
          <button>Toggle 4</button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className={`main-content ${selectedTicker ? 'expanded' : ''}`}>
        {/* Main Table */}
        <div className="main-table-container">
          <table className="main-table">
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Price</th>
                <th>Quantity</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((trade) => (
                <tr key={trade.id} onClick={() => setSelectedTicker(trade.ticker)}>
                  <td>{trade.ticker}</td>
                  <td>{trade.price}</td>
                  <td>{trade.quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Child Table Below Main Table */}
          {selectedTicker && (
            <table className="child-table">
              <thead>
                <tr>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{childData[selectedTicker]?.details}</td>
                </tr>
              </tbody>
            </table>
          )}
        </div>

        {/* Side Tables to the Right */}
        {selectedTicker && (
          <div className="side-tables">
            {/* First Side Table */}
            <div className="side-table">
              <table>
                <thead>
                  <tr>
                    <th>Additional Info 1</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>More details for {selectedTicker}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Second and Third Side Tables Stacked Below */}
            <div className="sub-side-tables">
              <div className="side-table">
                <table>
                  <thead>
                    <tr>
                      <th>Additional Info 2</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Extra details for {selectedTicker}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div className="side-table">
                <table>
                  <thead>
                    <tr>
                      <th>Additional Info 3</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Further details for {selectedTicker}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TradeDashboard;
