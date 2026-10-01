import type { DatabaseSchema, HistoryItem, NLToSQLResponse, SQLToNLResponse } from "../types";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api/v1${path}`, { headers: { "Content-Type": "application/json" }, ...init });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail ?? res.statusText));
  }
  return res.status === 204 ? (undefined as T) : res.json();
}
const post = (body: unknown): RequestInit => ({ method: "POST", body: JSON.stringify(body) });

export const api = {
  parseSchema: (ddl: string) => req<DatabaseSchema>("/schema/parse", post({ ddl })),
  nlToSql: (question: string, schema: DatabaseSchema) => req<NLToSQLResponse>("/nl-to-sql", post({ question, schema })),
  sqlToNl: (sql: string, schema: DatabaseSchema | null) => req<SQLToNLResponse>("/sql-to-nl", post({ sql, schema })),
  format: (sql: string, uppercase: boolean) => req<{ sql: string }>("/format", post({ sql, uppercase })),
  history: () => req<HistoryItem[]>("/history"),
  updateHistory: (id: number, patch: Partial<Pick<HistoryItem, "name" | "saved">>) =>
    req<HistoryItem>(`/history/${id}`, { method: "PATCH", body: JSON.stringify(patch) }),
  deleteHistory: (id: number) => req<void>(`/history/${id}`, { method: "DELETE" }),
};
