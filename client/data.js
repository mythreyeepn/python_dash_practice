const onFilterTextBoxChange = useCallback(() => {
  const filterValue = document.getElementById("filter-text-box").value;

  // Apply quick filter
  gridRef.current.api.setQuickFilter(filterValue);

  // Get filtered rows immediately
  const filteredRows = [];
  gridRef.current.api.forEachNodeAfterFilter(node => {
    filteredRows.push(node.data);
  });

  // Do whatever you want with the filtered rows
  console.log("Live filtered rows:", filteredRows);
  // Optionally: setFilteredRows(filteredRows); // if storing in state
}, []);
