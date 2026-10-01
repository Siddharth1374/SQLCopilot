"""Parse CREATE TABLE DDL into a structured DatabaseSchema (tables, PKs, FKs)."""
import sqlglot
from sqlglot import exp

from app.schemas.schema_models import Column, DatabaseSchema, Table


def parse_ddl(ddl: str) -> DatabaseSchema:
    tables: list[Table] = []
    for stmt in sqlglot.parse(ddl, read="mysql"):
        if not isinstance(stmt, exp.Create) or stmt.args.get("kind", "").upper() != "TABLE":
            continue
        schema_node = stmt.this
        table_name = schema_node.this.name
        cols: dict[str, Column] = {}
        for node in schema_node.expressions:
            if isinstance(node, exp.ColumnDef):
                col = Column(name=node.name, type=node.args["kind"].sql("mysql") if node.args.get("kind") else "")
                for c in node.args.get("constraints", []):
                    if isinstance(c.kind, exp.PrimaryKeyColumnConstraint):
                        col.is_primary_key = True
                cols[col.name.lower()] = col
            elif isinstance(node, exp.PrimaryKey):
                for e in node.expressions:
                    key = e.name.lower()
                    if key in cols:
                        cols[key].is_primary_key = True
            elif isinstance(node, exp.ForeignKey):
                ref = node.args.get("reference")
                if ref:
                    ref_table = ref.this.this.name
                    ref_cols = [c.name for c in ref.this.expressions]
                    for local, remote in zip((e.name for e in node.expressions), ref_cols):
                        if local.lower() in cols:
                            cols[local.lower()].references = f"{ref_table}.{remote}"
        tables.append(Table(name=table_name, columns=list(cols.values())))
    return DatabaseSchema(tables=tables)
