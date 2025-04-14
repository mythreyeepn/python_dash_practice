// App.jsx
import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [selectedRow, setSelectedRow] = useState(null);

  const handleRowClick = (index) => {
    setSelectedRow(index === selectedRow ? null : index);
  };

  const renderSmallTable = (title) => (
    <div className="small-table">
      <div className="row">{title} - Row 1</div>
      <div className="row">{title} - Row 2</div>
    </div>
  );

//   valueFormatter: (params) => {
//     const date = new Date(params.value);
//     if (!params.value) return '';
//     const pad = (n) => String(n).padStart(2, '0');
//     return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}  ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
//   }

  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="navbar-left">My App</div>
        <div className="navbar-right">
          <label className="switch">
            <input type="checkbox" />
            <span className="slider round"></span>
          </label>
          <label className="switch">
            <input type="checkbox" />
            <span className="slider round"></span>
          </label>
          <label className="switch">
            <input type="checkbox" />
            <span className="slider round"></span>
          </label>
        </div>
      </nav>
      <div className="main-layout">
        <div className="left-content">
          <div className="main-table">
            {[...Array(20)].map((_, i) => (
              <div
                key={i}
                className={`row ${selectedRow === i ? 'selected' : ''}`}
                onClick={() => handleRowClick(i)}
              >
                Row {i + 1}
              </div>
            ))}
          </div>
          {selectedRow !== null && (
            <div className="child-table">
              <div>Child Table for Row {selectedRow + 1}</div>
              <div className="row">Child Row A</div>
              <div className="row">Child Row B</div>
            </div>
          )}
        </div>
        {selectedRow !== null && (
          <div className="side-tables">
            {renderSmallTable('Small Table 1')}
            {renderSmallTable('Small Table 2')}
            {renderSmallTable('Small Table 3')}
            {renderSmallTable('Small Table 4')}
          </div>
        )}
      </div>
    </div>
  );
};

export default App; // App.css

body {
  margin: 0;
  font-family: sans-serif;
}

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.navbar {
  background-color: #242120;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
  height: 60px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.navbar-left {
  font-size: 1.2rem;
}

.navbar-right {
  display: flex;
  gap: 10px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.main-layout {
  display: flex;
  flex: 1;
  padding-top: 60px; /* height of navbar */
  overflow: hidden;
}

.left-content {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.side-tables {
  width: 250px;
  background: #f1f1f1;
  overflow-y: auto;
  padding: 1rem;
  border-left: 1px solid #ccc;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.main-table, .child-table {
  background: #fff;
  border: 1px solid #ddd;
  margin-bottom: 1rem;
}

.row {
  padding: 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.row:hover {
  background: #f9f9f9;
}

.selected {
  background: #d9eaff;
}

.small-table {
  background: white;
  border: 1px solid #ccc;
  padding: 0.5rem;
  min-height: 80px;
}
