let socket = null;
let reconnectInterval = 3000; // 3 seconds
const traderChannel = "trader-skews"; // use dynamic trader ID if needed

function connectWebSocket() {
  socket = new WebSocket(`ws://localhost:8000/ws/${traderChannel}`);

  socket.onopen = () => {
    console.log("[WS] Connected to trader-skews");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    switch (data.event) {
      case "skew_updated":
        console.log("[WS] Skew updated:", data);
        gridRef.api.applyTransaction({
          update: [{ isin: data.isin, [data.column]: data.new_value }]
        });
        break;

      case "start_edit":
        showEditorTooltip(data.isin, data.column, data.username);
        break;

      case "stop_edit":
        hideEditorTooltip(data.isin, data.column);
        break;

      default:
        console.log("[WS] Unknown event:", data);
    }
  };

  socket.onclose = (e) => {
    console.warn(`[WS] Disconnected. Attempting to reconnect in ${reconnectInterval / 1000}s`, e.reason);
    setTimeout(connectWebSocket, reconnectInterval);
  };

  socket.onerror = (err) => {
    console.error("[WS] Error:", err.message);
    socket.close();
  };
}

// Call this once (e.g., on app load or after selecting trader)
connectWebSocket();


onCellEditingStarted: (event) => {
  socket.send(JSON.stringify({
    event: "start_edit",
    isin: event.data.isin,
    column: event.colDef.field,
    user_id: currentUser.id,
    username: currentUser.name
  }));
},


onCellEditingStopped: (event) => {
  socket.send(JSON.stringify({
    event: "stop_edit",
    isin: event.data.isin,
    column: event.colDef.field,
    user_id: currentUser.id
  }));
}


