const handleUndo = async () => {
  try {
    const response = await axios.post("/skews_undo", {
      user_id: currentUser.id
    });

    const { reverted, conflicts } = response.data;

    if (conflicts.length > 0) {
      conflicts.forEach((item) => {
        console.warn(
          `Undo skipped for ${item.isin} (${item.column}): ${item.reason}`
        );
        // Optionally mark conflict visually
        const rowNode = gridRef.current.api.getRowNode(item.isin);
        if (rowNode) {
          const updated = { ...rowNode.data };
          updated.conflictColumns = {
            ...(updated.conflictColumns || {}),
            [item.column]: true
          };
          gridRef.current.api.applyTransaction({ update: [updated] });
        }
      });
      alert("Undo applied partially. Some values were skipped due to conflict.");
    } else {
      console.log("Undo successful:", reverted);
    }
  } catch (err) {
    console.error("Undo failed:", err.response?.data?.detail || err.message);
    alert("Nothing left to undo or an error occurred.");
  }
};