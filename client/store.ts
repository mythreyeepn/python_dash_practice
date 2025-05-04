import create from 'zustand';

interface Bond {
  sector: string;
  maturity: string;
  rating: string;
  ticker: string;
  isin: string;
  buySkew: string;
  sellSkew: string;
  dnt: string;
}

interface BondStore {
  traders: { id: string; name: string }[];
  selectedTrader: { id: string; name: string } | null;
  setTraders: (traders: { id: string; name: string }[]) => void;
  setSelectedTrader: (trader: { id: string; name: string } | null) => void;
  bonds: Bond[];
  setBonds: (bonds: Bond[]) => void;
}

export const useBondStore = create<BondStore>((set) => ({
  traders: [],
  selectedTrader: null,
  setTraders: (traders) => set({ traders }),
  setSelectedTrader: (selectedTrader) => set({ selectedTrader }),
  bonds: [],
  setBonds: (bonds) => set({ bonds }),
}));



// src/store/bondStore.ts
import { create } from 'zustand';

export type Bond = {
  isin: string;
  trader: string;
  ticker: string;
  sector: string;
  maturity: string;
  rating: string;
  buySkew?: number;
  sellSkew?: number;
  dnt?: number;
};

type BondStore = {
  allBonds: Bond[];
  filteredBonds: Bond[];
  selectedTrader: string;
  setAllBonds: (bonds: Bond[]) => void;
  setTrader: (trader: string) => void;
  updateBond: (isin: string, patch: Partial<Bond>) => void;
  bulkUpdate: (patch: Partial<Bond>, filterFn: (bond: Bond) => boolean) => void;
};

export const useBondStore = create<BondStore>((set, get) => ({
  allBonds: [],
  filteredBonds: [],
  selectedTrader: '',

  setAllBonds: (bonds) => set(() => ({ allBonds: bonds, filteredBonds: bonds })),

  setTrader: (trader) => {
    const all = get().allBonds;
    set({
      selectedTrader: trader,
      filteredBonds: all.filter((b) => b.trader === trader),
    });
  },

  updateBond: (isin, patch) => {
    const all = get().allBonds.map((b) =>
      b.isin === isin ? { ...b, ...patch } : b
    );
    const trader = get().selectedTrader;
    set({
      allBonds: all,
      filteredBonds: all.filter((b) => b.trader === trader),
    });
  },

  bulkUpdate: (patch, filterFn) => {
    const all = get().allBonds.map((b) =>
      filterFn(b) ? { ...b, ...patch } : b
    );
    const trader = get().selectedTrader;
    set({
      allBonds: all,
      filteredBonds: all.filter((b) => b.trader === trader),
    });
  },
}));
