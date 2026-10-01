"""Validate SQL against the parsed schema (tables + columns exist)."""
from sqlglot import exp

from app.schemas.responses import Check, ValidationResult
from app.schemas.schema_models import DatabaseSchema
from app.services import sql_parser


def validate(sql: str, schema: DatabaseSchema) -> ValidationResult:
    checks: list[Check] = []
    errors: list[str] = []
    try:
        tree = sql_parser.parse(sql)
    except sql_parser.SQLParseError as e:
        return ValidationResult(valid=False, checks=[Check(label="Syntax is valid", ok=False)], errors=[str(e)])
    checks.append(Check(label="Syntax is valid", ok=True))

    alias_map = sql_parser.referenced_tables(tree)
    cte_names = {c.alias.lower() for c in tree.find_all(exp.CTE)}
    for alias, real in alias_map.items():
        if real.lower() in cte_names:
            continue
        ok = real.lower() in schema.table_names()
        checks.append(Check(label=f"Table `{real}` exists", ok=ok))
        if not ok:
            errors.append(f"Unknown table: {real}")

    select_aliases = {a.alias.lower() for a in tree.find_all(exp.Alias)}
    all_cols = {c for t in schema.tables for c in schema.columns_of(t.name)}
    seen: set[tuple] = set()
    for qualifier, col in sql_parser.referenced_columns(tree):
        if col == "*" or (qualifier, col) in seen:
            continue
        seen.add((qualifier, col))
        if qualifier:
            real = alias_map.get(qualifier.lower())
            ok = bool(real) and col.lower() in schema.columns_of(real)
        else:
            ok = col.lower() in all_cols or col.lower() in select_aliases
        checks.append(Check(label=f"Column `{col}` exists", ok=ok))
        if not ok:
            errors.append(f"Unknown column: {(qualifier + '.') if qualifier else ''}{col}")
    return ValidationResult(valid=not errors, checks=checks, errors=errors)
