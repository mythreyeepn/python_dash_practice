import create from 'zustand'

interface Bond {
  isin: string
  ticker: string
  sector: string
  maturity: string
  rating: string
  buySkew: number
  sellSkew: number
  dnt: number
  bondType: string
  traderId: string
}

interface Trader {
  id: string
  name: string
}

interface BondStore {
  bonds: Bond[]
  traders: Trader[]
  setBonds: (bonds: Bond[]) => void
  setTraders: (traders: Trader[]) => void
}

export const useBondStore = create<BondStore>((set) => ({
  bonds: [],
  traders: [],
  setBonds: (bonds) => set({ bonds }),
  setTraders: (traders) => set({ traders }),
}))
