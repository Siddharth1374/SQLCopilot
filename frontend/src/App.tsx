import { useEffect, useState } from "react";
import { api } from "./api/client";
import HistoryPanel from "./components/HistoryPanel";
import ResultPanel from "./components/ResultPanel";
import SchemaPanel from "./components/SchemaPanel";
import SqlEditor from "./components/SqlEditor";
import { useAppStore } from "./store/useAppStore";
import type { NLToSQLResponse, SQLToNLResponse } from "./types";

export default function App() {
  const { schema, dark, uppercase, toggleDark, toggleCase } = useAppStore();
  const [mode, setMode] = useState<"nl" | "sql">("nl");
  const [question, setQuestion] = useState("");
  const [sql, setSql] = useState("");
  const [nlResult, setNlResult] = useState<NLToSQLResponse | null>(null);
  const [sqlResult, setSqlResult] = useState<SQLToNLResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => { document.documentElement.classList.toggle("dark", dark); }, [dark]);

  const run = async () => {
    setError(""); setLoading(true);
    try {
      if (mode === "nl") {
        if (!schema) throw new Error("Load a schema first");
        const r = await api.nlToSql(question, schema);
        setNlResult(r);
        setSql((await api.format(r.sql, uppercase)).sql);
      } else {
        setSqlResult(await api.sqlToNl(sql, schema));
      }
      setRefreshKey((k) => k + 1);
    } catch (e) { setError((e as Error).message); }
    finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-white text-slate-900 dark:bg-slate-900 dark:text-slate-100">
      <header className="flex items-center justify-between border-b p-4">
        <h1 className="text-xl font-bold">SQL Translator</h1>
        <div className="flex gap-2 text-sm">
          <button onClick={toggleCase} className="rounded border px-2 py-1">{uppercase ? "UPPER" : "lower"}</button>
          <button onClick={toggleDark} className="rounded border px-2 py-1">{dark ? "Light" : "Dark"}</button>
        </div>
      </header>
      <main className="grid gap-6 p-4 lg:grid-cols-[320px_1fr_320px]">
        <SchemaPanel />
        <section className="space-y-3">
          <div className="flex gap-2">
            <button onClick={() => setMode("nl")} className={mode === "nl" ? "font-bold underline" : ""}>Text → SQL</button>
            <button onClick={() => setMode("sql")} className={mode === "sql" ? "font-bold underline" : ""}>SQL → Text</button>
          </div>
          {mode === "nl" && (
            <textarea value={question} onChange={(e) => setQuestion(e.target.value)} rows={3}
              placeholder="Show employees whose salary > 50000" className="w-full rounded border p-2 dark:bg-slate-800" />
          )}
          <SqlEditor value={sql} onChange={setSql} readOnly={mode === "nl"} />
          <button onClick={run} disabled={loading} className="rounded bg-indigo-600 px-4 py-2 text-white disabled:opacity-50">
            {loading ? "Working..." : "Translate"}
          </button>
          {error && <p className="text-red-500">{error}</p>}
          {mode === "nl" && nlResult && <ResultPanel r={nlResult} />}
          {mode === "sql" && sqlResult && (
            <div className="space-y-2 text-sm">
              <p>→ {sqlResult.explanation}</p>
              <ol className="list-decimal pl-5">{sqlResult.steps.map((s, i) => <li key={i}>{s}</li>)}</ol>
              {sqlResult.optimizations.map((o, i) => <p key={i} className="text-amber-600">⚠ {o}</p>)}
            </div>
          )}
        </section>
        <HistoryPanel refreshKey={refreshKey} onLoad={(s) => { setMode("sql"); setSql(s); }} />
      </main>
    </div>
  );
}
