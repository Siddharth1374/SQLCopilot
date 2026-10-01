# SQL Translator

Bidirectional **SQL ⇄ Natural Language** translator with schema-aware generation, validation,
explanations, optimization hints and a safety layer. MySQL dialect.

## Architecture

```
React + TS (Vite, Tailwind, Monaco)
        │  /api/v1
        ▼
FastAPI ── routes ──► services
                       ├─ schema_service  DDL → structured schema (tables, PK, FK)
                       ├─ sql_parser      sqlglot AST + intermediate representation (IR)
                       ├─ llm_service     Groq (receives schema text only, never DB creds)
                       ├─ validator       tables / columns exist
                       ├─ safety          DROP / DELETE / TRUNCATE / UPDATE w/o WHERE, read-only mode
                       ├─ optimizer       index & LIMIT hints
                       ├─ explainer       IR → step-by-step English (deterministic)
                       ├─ formatter       pretty-print, upper/lower case
                       ├─ executor        optional read-only MySQL execution
                       └─ history_service save / rename / delete (SQLite)
```

**NL → SQL:** question + schema → Groq → parse → validate → safety → explain → optimize  
**SQL → NL:** SQL → parse → IR → deterministic steps (+ LLM one-line summary)

## Quick start

```bash
cp .env.example .env            # add GROQ_API_KEY
make up                         # docker: backend :8000, frontend :5173, MySQL :3306
# or locally
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload
cd frontend && npm install && npm run dev
```

API docs: http://localhost:8000/docs · Tests: `make test`

## Security notes
- `READ_ONLY_MODE=true` by default; non-SELECT statements are blocked at `/execute`.
- Use a MySQL user with **SELECT-only** grants for `TARGET_DB_URL`.
- The LLM sees schema text only. Execution always goes through validator + safety.
