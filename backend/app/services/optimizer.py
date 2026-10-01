"""Rule-based optimization hints."""
from sqlglot import exp

from app.schemas.schema_models import DatabaseSchema
from app.services import sql_parser


def suggest(sql: str, schema: DatabaseSchema | None = None) -> list[str]:
    tips: list[str] = []
    try:
        tree = sql_parser.parse(sql)
    except sql_parser.SQLParseError:
        return tips
    alias_map = sql_parser.referenced_tables(tree)

    if tree.find(exp.Star):
        tips.append("Avoid SELECT *; list only the columns you need.")
    for join in tree.find_all(exp.Join):
        on = join.args.get("on")
        if on:
            for col in on.find_all(exp.Column):
                real = alias_map.get((col.table or "").lower(), col.table)
                if real and col.name.lower() != "id":
                    tips.append(f"Consider an index on {real}.{col.name} (used in JOIN).")
    where = tree.find(exp.Where)
    if where:
        for col in where.find_all(exp.Column):
            real = alias_map.get((col.table or "").lower()) or next(iter(alias_map.values()), None)
            if real:
                tips.append(f"Consider an index on {real}.{col.name} (used in WHERE).")
        if where.find(exp.Like) and "'%" in where.sql("mysql"):
            tips.append("A leading wildcard in LIKE prevents index use.")
    if isinstance(tree, exp.Select) and not tree.args.get("limit") and not tree.find(exp.AggFunc):
        tips.append("Consider adding LIMIT for large tables.")
    return list(dict.fromkeys(tips))
