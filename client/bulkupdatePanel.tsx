const response = await axios.post(...);

// Only this client gets the conflict info
response.data.updated.forEach((item) => {
  const rowNode = gridRef.current.api.getRowNode(item.isin);
  if (!rowNode) return;

  const fullRow = { ...rowNode.data };
  fullRow[item.column] = item.new_value;

  // ✅ Red border if conflict
  if (item.conflict) {
    fullRow.conflictColumns = {
      ...(fullRow.conflictColumns || {}),
      [item.column]: true
    };
    // Optional auto-clear
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


.cell-red-border {
  border: 2px solid red !important;
}

'cell-red-border': (params) => {
  return params.data.conflictColumns?.[params.colDef.field] === true;
}