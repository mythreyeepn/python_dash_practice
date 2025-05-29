import React, { useState, useEffect, useRef } from "react";
import { Backdrop, CircularProgress } from "@mui/material";
import axios from "axios";
import AGGridComponent from "./AGGridComponent"; // Assume your grid component

const BulkUpdateComponent = ({ selectedUser }) => {
  const [bulk_skew, setBulkSkew] = useState("Select");
  const [bulk_crb_mode, setBulkCrbMode] = useState("Select");
  const [loading, setLoading] = useState(false);
  const gridRef = useRef(null);

  useEffect(() => {
    const traderChannel = "trader-skews";
    const socket = new WebSocket(`ws://localhost:8001/ws/${traderChannel}`);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const color = data.user_id === selectedUser ? "green" : "blue";
      const expiresAt = Date.now() + 15000;

      switch (data.event) {
        case "skew_updated":
          if (gridRef.current) {
            const rowNode = gridRef.current.api.getRowNode(data.isin);
            if (!rowNode) break;

            const fullRow = { ...rowNode.data };
            fullRow[data.column] = data.new_value;
            fullRow["last_updated_by"] = data.user_id;
            fullRow["last_updated_at"] = data.timestamp;

            fullRow.highlightStatus = {
              ...(fullRow.highlightStatus || {}),
              [data.column]: {
                color: data.highlight?.color || color,
                expiresAt,
              },
            };

            gridRef.current.api.applyTransaction({
              update: [fullRow],
            });
          }
          break;

        default:
          console.log("[WS] Unknown event:", data);
      }
    };

    return () => socket.close();
  }, [selectedUser]);

  const handleBulkUpdate = async () => {
    const updates = [];
    const clientLastSeenMap = {};

    gridRef.current.api.forEachNodeAfterFilterAndSort((node) => {
      const { isin, last_updated_at } = node.data;
      if (bulk_skew !== "Select") {
        updates.push({ isin, column: "skew", new_value: bulk_skew });
      }
      if (bulk_crb_mode !== "Select") {
        updates.push({ isin, column: "crb_mode", new_value: bulk_crb_mode });
      }
      if (last_updated_at) {
        clientLastSeenMap[isin] = last_updated_at;
      }
    });

    if (updates.length === 0) return;

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8001/skews_bulk_update", {
        updates,
        user_id: selectedUser,
        client_last_seen_map: clientLastSeenMap,
      });

      response.data.updated.forEach((item) => {
        const rowNode = gridRef.current.api.getRowNode(item.isin);
        if (!rowNode) return;

        const fullRow = { ...rowNode.data };
        fullRow[item.column] = item.new_value;

        if (item.conflict) {
          fullRow.conflictColumns = {
            ...(fullRow.conflictColumns || {}),
            [item.column]: true,
          };

          setTimeout(() => {
            const r = gridRef.current.api.getRowNode(item.isin)?.data;
            if (!r) return;
            const updated = { ...r };
            updated.conflictColumns[item.column] = false;
            gridRef.current.api.applyTransaction({ update: [updated] });
          }, 45000);
        }

        gridRef.current.api.applyTransaction({ update: [fullRow] });
      });
    } catch (err) {
      console.error("Bulk update error:", err);
    } finally {
      setLoading(false);
      setBulkSkew("Select");
      setBulkCrbMode("Select");
    }
  };

  return (
    <>
      <Backdrop open={loading} sx={{ zIndex: 2000 }}>
        <CircularProgress color="inherit" />
      </Backdrop>

      <AGGridComponent gridRef={gridRef} />

      {/* Bulk controls */}
      <div style={{ marginTop: 10 }}>
        <select value={bulk_skew} onChange={(e) => setBulkSkew(e.target.value)}>
          <option value="Select">Select Skew</option>
          <option value="Buy">Buy</option>
          <option value="Strong Buy">Strong Buy</option>
          <option value="Sell">Sell</option>
          <option value="Strong Sell">Strong Sell</option>
          <option value="Neutral">Neutral</option>
        </select>

        <select value={bulk_crb_mode} onChange={(e) => setBulkCrbMode(e.target.value)}>
          <option value="Select">Select CRB Mode</option>
          <option value="Do Not Trade">Do Not Trade</option>
          <option value="Buy Only">Buy Only</option>
          <option value="Sell Only">Sell Only</option>
          <option value="Risk Reduce Only">Risk Reduce Only</option>
          <option value="Risk Reduce Buy Only">Risk Reduce Buy Only</option>
          <option value="Risk Reduce Sell Only">Risk Reduce Sell Only</option>
          <option value="Market Make">Market Make</option>
        </select>

        <button onClick={handleBulkUpdate}>Apply Bulk Update</button>
      </div>
    </>
  );
};

export default BulkUpdateComponent;
