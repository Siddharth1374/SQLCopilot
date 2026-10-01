"""Read-only execution against the optional target MySQL database."""
from sqlalchemy import create_engine, text

from app.core.config import settings


def execute_readonly(sql: str) -> dict:
    if not settings.target_db_url:
        raise RuntimeError("TARGET_DB_URL is not configured")
    engine = create_engine(
        settings.target_db_url,
        connect_args={"read_timeout": settings.query_timeout_seconds},
    )
    with engine.connect() as conn:
        conn.exec_driver_sql("SET SESSION TRANSACTION READ ONLY")
        result = conn.execute(text(sql))
        rows = result.fetchmany(settings.max_rows)
        return {"columns": list(result.keys()), "rows": [list(r) for r in rows], "truncated": len(rows) == settings.max_rows}
