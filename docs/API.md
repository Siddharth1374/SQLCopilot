| Method | Path | Purpose |
|---|---|---|
| POST | /api/v1/schema/parse | DDL → schema JSON |
| POST | /api/v1/nl-to-sql | question + schema → SQL, validation, safety, explanation, tips |
| POST | /api/v1/sql-to-nl | SQL → summary + steps + tips |
| POST | /api/v1/validate | validate SQL against schema |
| POST | /api/v1/format | format / case toggle |
| POST | /api/v1/execute | read-only execution (confirmation for risky SQL) |
| GET/PATCH/DELETE | /api/v1/history[/id] | query history |
