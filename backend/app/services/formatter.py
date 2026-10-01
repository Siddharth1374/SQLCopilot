import sqlglot


def format_sql(sql: str, uppercase: bool = True) -> str:
    out = sqlglot.transpile(sql, read="mysql", write="mysql", pretty=True)[0]
    if not uppercase:
        # keep identifiers/strings intact; only lowercase the pretty output keywords is non-trivial,
        # so we re-generate with normalize and lowercase via a safe pass.
        out = sqlglot.parse_one(sql, read="mysql").sql(dialect="mysql", pretty=True, identify=False)
        return _lower_keywords(out)
    return out


def _lower_keywords(sql: str) -> str:
    import re
    kws = r"\b(SELECT|FROM|WHERE|JOIN|LEFT|RIGHT|INNER|OUTER|ON|GROUP BY|ORDER BY|HAVING|LIMIT|AND|OR|AS|COUNT|SUM|AVG|MIN|MAX|DESC|ASC|IN|NOT|NULL|LIKE|DISTINCT)\b"
    return re.sub(kws, lambda m: m.group(0).lower(), sql)
