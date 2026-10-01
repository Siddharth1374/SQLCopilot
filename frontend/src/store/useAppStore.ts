import { create } from "zustand";
import type { DatabaseSchema } from "../types";

interface State {
  schema: DatabaseSchema | null;
  dark: boolean;
  uppercase: boolean;
  setSchema: (s: DatabaseSchema | null) => void;
  toggleDark: () => void;
  toggleCase: () => void;
}

export const useAppStore = create<State>((set) => ({
  schema: null,
  dark: true,
  uppercase: true,
  setSchema: (schema) => set({ schema }),
  toggleDark: () => set((s) => ({ dark: !s.dark })),
  toggleCase: () => set((s) => ({ uppercase: !s.uppercase })),
}));
