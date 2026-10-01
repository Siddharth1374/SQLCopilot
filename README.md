# SQL Translator

Bidirectional **SQL ⇄ Natural Language** translator with schema-aware generation, validation,
explanations, optimization hints .
<img width="1897" height="857" alt="image" src="https://github.com/user-attachments/assets/198a1ae8-67ea-4f14-9d38-b713b1b5f143" />

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

