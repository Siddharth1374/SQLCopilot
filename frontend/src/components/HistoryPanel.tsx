import { useEffect, useState } from "react";
import { api } from "../api/client";
import { copy } from "../lib/clipboard";
import type { HistoryItem } from "../types";

export default function HistoryPanel({ refreshKey, onLoad }: { refreshKey: number; onLoad: (sql: string) => void }) {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const load = () => api.history().then(setItems).catch(() => {});
  useEffect(() => { load(); }, [refreshKey]);

  return (
    <section className="space-y-2">
      <h2 className="font-semibold">History</h2>
      {items.map((h) => (
        <div key={h.id} className="rounded border p-2 text-xs">
          <p className="font-medium">{h.name || h.natural_language.slice(0, 60)}</p>
          <pre className="overflow-x-auto">{h.sql}</pre>
          <div className="mt-1 flex gap-2">
            <button onClick={() => onLoad(h.sql)}>Open</button>
            <button onClick={() => copy(h.sql)}>Copy</button>
            <button onClick={() => { const name = prompt("Rename", h.name); if (name !== null) api.updateHistory(h.id, { name, saved: true }).then(load); }}>Rename</button>
            <button onClick={() => api.deleteHistory(h.id).then(load)}>Delete</button>
          </div>
        </div>
      ))}
    </section>
  );
}
