// src/components/BulkUpdatePanel.tsx
import React, { useState } from 'react';
import { useBondStore } from '../store/bondStore';

const BulkUpdatePanel = () => {
  const { bulkUpdate, filteredBonds } = useBondStore();
  const [buySkew, setBuySkew] = useState<number | string>('');
  const [sellSkew, setSellSkew] = useState<number | string>('');
  const [dnt, setDnt] = useState<number | string>('');

  const handleBulkUpdate = () => {
    const patch: Partial<Bond> = {};
    if (buySkew) patch.buySkew = Number(buySkew);
    if (sellSkew) patch.sellSkew = Number(sellSkew);
    if (dnt) patch.dnt = Number(dnt);

    bulkUpdate(patch, (bond) => filteredBonds.includes(bond));
  };

  return (
    <div className="mb-4">
      <div>
        <label htmlFor="buySkew">Buy Skew:</label>
        <input
          id="buySkew"
          type="number"
          value={buySkew}
          onChange={(e) => setBuySkew(e.target.value)}
          className="ml-2 p-1 border"
        />
      </div>
      <div>
        <label htmlFor="sellSkew">Sell Skew:</label>
        <input
          id="sellSkew"
          type="number"
          value={sellSkew}
          onChange={(e) => setSellSkew(e.target.value)}
          className="ml-2 p-1 border"
        />
      </div>
      <div>
        <label htmlFor="dnt">DNT:</label>
        <input
          id="dnt"
          type="number"
          value={dnt}
          onChange={(e) => setDnt(e.target.value)}
          className="ml-2 p-1 border"
        />
      </div>
      <button onClick={handleBulkUpdate} className="mt-2 p-2 bg-blue-500 text-white">
        Update Selected
      </button>
    </div>
  );
};

export default BulkUpdatePanel;
