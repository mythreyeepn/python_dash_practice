
const handleSkewChange = async (event) => {
  const { data, colDef, newValue, oldValue } = event;
  if (newValue === oldValue) return;

  await axios.post("/skews/update", {
    isin: data.isin,
    column: colDef.field,
    new_value: parseFloat(newValue),
    user_id: currentUser.id,
    client_last_seen: data.last_updated_at
  });
};

const socket = new WebSocket("ws://localhost:8000/ws");

socket.onmessage = (msg) => {
  const data = JSON.parse(msg.data);
  if (data.event === "skew_updated") {
    gridRef.api.applyTransaction({ update: [{ isin: data.isin, [data.column]: data.new_value }] });
  }
  if (data.event === "start_edit") {
    showEditorTooltip(data.isin, data.column, data.username);
  }
  if (data.event === "stop_edit") {
    hideEditorTooltip(data.isin, data.column);
  }
};

function showEditorTooltip(isin, column, username) {
  const cell = document.querySelector(`[row-isin='${isin}'] [col-id='${column}']`);
  if (cell) {
    const tooltip = document.createElement("div");
    tooltip.className = "cell-tooltip";
    tooltip.innerText = `${username} is editing...`;
    cell.appendChild(tooltip);
  }
}

function hideEditorTooltip(isin, column) {
  const cell = document.querySelector(`[row-isin='${isin}'] [col-id='${column}']`);
  if (cell) {
    const tooltip = cell.querySelector(".cell-tooltip");
    if (tooltip) tooltip.remove();
  }
}