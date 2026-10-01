"""Deterministic step-by-step explanation from the IR (the LLM only polishes the summary)."""


def steps_from_ir(ir: dict) -> list[str]:
    if ir.get("type") != "select":
        return [f"This is a {ir.get('type', 'SQL')} statement."]
    steps: list[str] = []
    if ir["from"]:
        steps.append(f"FROM: start with the `{ir['from']}` table.")
    for j in ir["joins"]:
        on = f" matching rows where {j['on']}" if j["on"] else ""
        steps.append(f"{j['kind']} JOIN: combine with `{j['table']}`{on}.")
    if ir["where"]:
        steps.append(f"WHERE: keep only rows where {ir['where']}.")
    if ir["group_by"]:
        steps.append(f"GROUP BY: group rows by {', '.join(ir['group_by'])}.")
    if ir["having"]:
        steps.append(f"HAVING: keep only groups where {ir['having']}.")
    d = "unique " if ir["distinct"] else ""
    steps.append(f"SELECT: return the {d}values {', '.join(ir['columns'])}.")
    if ir["order_by"]:
        steps.append(f"ORDER BY: sort by {', '.join(ir['order_by'])}.")
    if ir["limit"]:
        steps.append(f"LIMIT: return at most {ir['limit']} rows.")
    return steps
