import { useState } from "react";
import { api } from "../api/client";
import { useAppStore } from "../store/useAppStore";

export default function SchemaPanel() {
  const { schema, setSchema } = useAppStore();
  const [ddl, setDdl] = useState("");
  const [err, setErr] = useState("");

  const load = async () => {
    try { setSchema(await api.parseSchema(ddl)); setErr(""); }
    catch (e) { setErr((e as Error).message); }
  };

  return (
    <section className="space-y-2">
      <h2 className="font-semibold">Schema</h2>
      <textarea value={ddl} onChange={(e) => setDdl(e.target.value)} rows={6}
        placeholder="Paste CREATE TABLE statements..." className="w-full rounded border p-2 font-mono text-xs dark:bg-slate-800" />
      <button onClick={load} className="rounded bg-indigo-600 px-3 py-1 text-white">Parse schema</button>
      {err && <p className="text-sm text-red-500">{err}</p>}
      {schema && (
        <ul className="text-sm font-mono">
          {schema.tables.map((t) => (
            <li key={t.name}>
              <b>{t.name}</b>
              <ul className="ml-4">
                {t.columns.map((c) => (
                  <li key={c.name}>{c.name} {c.is_primary_key && "PK"} {c.references && `FK → ${c.references}`}</li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
