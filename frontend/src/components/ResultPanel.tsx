import { copy } from "../lib/clipboard";
import type { NLToSQLResponse } from "../types";

export default function ResultPanel({ r }: { r: NLToSQLResponse }) {
  return (
    <div className="space-y-3 text-sm">
      <ul>
        {r.validation.checks.map((c, i) => <li key={i}>{c.ok ? "✓" : "✗"} {c.label}</li>)}
      </ul>
      {r.safety.findings.length > 0 && (
        <div className="rounded border border-red-400 bg-red-50 p-2 text-red-700 dark:bg-red-950 dark:text-red-300">
          {r.safety.findings.map((f, i) => <p key={i}>⚠ {f}</p>)}
        </div>
      )}
      {r.explanation && <p>→ {r.explanation}</p>}
      {r.optimizations.map((o, i) => <p key={i} className="text-amber-600">⚠ {o}</p>)}
      <button onClick={() => copy(r.sql)} className="rounded border px-2 py-1">Copy SQL</button>
    </div>
  );
}
