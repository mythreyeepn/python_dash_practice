const handleBulkUpdate = async () => {
  const updates = [];
  const clientLastSeenMap = {};

  gridRef.current.api.forEachNodeAfterFilterAndSort((node) => {
    const { isin, last_updated_at } = node.data;

    if (buySkew) {
      updates.push({
        isin,
        column: "buy_skew",
        new_value: Number(buySkew)
      });
    }

    if (sellSkew) {
      updates.push({
        isin,
        column: "sell_skew",
        new_value: Number(sellSkew)
      });
    }

    if (last_updated_at) {
      clientLastSeenMap[isin] = last_updated_at;
    }
  });

  if (updates.length === 0) return;

  await axios.post("/skews_bulk_update", {
    updates,
    user_id: currentUser.id,
    client_last_seen_map: clientLastSeenMap
  });

  setBuySkew('');
  setSellSkew('');
};