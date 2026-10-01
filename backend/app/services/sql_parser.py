"""AST helpers built on sqlglot (MySQL dialect)."""
import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError


class SQLParseError(Exception):
    pass


def parse(sql: str) -> exp.Expression:
    try:
        tree = sqlglot.parse_one(sql, read="mysql")
    except ParseError as e:
        raise SQLParseError(str(e)) from e
    if tree is None:
        raise SQLParseError("Empty query")
    return tree


def referenced_tables(tree: exp.Expression) -> dict[str, str]:
    """alias/name (lower) -> real table name."""
    out: dict[str, str] = {}
    for t in tree.find_all(exp.Table):
        out[(t.alias or t.name).lower()] = t.name
    return out


def referenced_columns(tree: exp.Expression) -> list[tuple[str | None, str]]:
    return [(c.table or None, c.name) for c in tree.find_all(exp.Column)]


def build_ir(tree: exp.Expression) -> dict:
    """Intermediate representation used for deterministic SQL -> NL explanations."""
    select = tree if isinstance(tree, exp.Select) else tree.find(exp.Select)
    if select is None:
        return {"type": tree.key}
    ir: dict = {
        "type": "select",
        "columns": [e.sql("mysql") for e in select.expressions],
        "from": None,
        "joins": [],
        "where": None,
        "group_by": [],
        "having": None,
        "order_by": [],
        "limit": None,
        "distinct": bool(select.args.get("distinct")),
    }
    frm = select.args.get("from")
    if frm:
        ir["from"] = frm.this.sql("mysql")
    for j in select.args.get("joins") or []:
        ir["joins"].append(
            {"kind": (j.args.get("kind") or "INNER").upper(), "table": j.this.sql("mysql"),
             "on": j.args["on"].sql("mysql") if j.args.get("on") else None}
        )
    if select.args.get("where"):
        ir["where"] = select.args["where"].this.sql("mysql")
    if select.args.get("group"):
        ir["group_by"] = [e.sql("mysql") for e in select.args["group"].expressions]
    if select.args.get("having"):
        ir["having"] = select.args["having"].this.sql("mysql")
    if select.args.get("order"):
        ir["order_by"] = [e.sql("mysql") for e in select.args["order"].expressions]
    if select.args.get("limit"):
        ir["limit"] = select.args["limit"].expression.sql("mysql")
    return ir
