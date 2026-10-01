"""Safety layer: detect destructive statements before anything is executed."""
from sqlglot import exp

from app.schemas.responses import SafetyReport
from app.services import sql_parser


def analyze(sql: str, read_only: bool = True) -> SafetyReport:
    findings: list[str] = []
    high = False
    try:
        tree = sql_parser.parse(sql)
    except sql_parser.SQLParseError:
        return SafetyReport(safe=False, risk_level="high", findings=["Query could not be parsed"], requires_confirmation=True)

    if tree.find(exp.Drop):
        findings.append("DROP statement detected"); high = True
    if isinstance(tree, exp.TruncateTable) or tree.find(exp.TruncateTable):
        findings.append("TRUNCATE statement detected"); high = True
    if isinstance(tree, exp.Delete):
        findings.append("DELETE statement detected"); high = True
        if not tree.args.get("where"):
            findings.append("DELETE without WHERE removes ALL rows")
    if isinstance(tree, exp.Update):
        findings.append("UPDATE statement detected")
        if not tree.args.get("where"):
            findings.append("UPDATE without WHERE changes ALL rows"); high = True
    if tree.find(exp.Alter):
        findings.append("ALTER statement detected"); high = True
    if isinstance(tree, (exp.Insert,)):
        findings.append("INSERT statement detected")

    is_read = isinstance(tree, (exp.Select, exp.Union, exp.Describe, exp.Show))
    if read_only and not is_read:
        findings.append("Read-only mode: only SELECT queries may be executed")
        high = True
    return SafetyReport(
        safe=not findings,
        risk_level="high" if high else ("low" if findings else "none"),
        findings=findings,
        requires_confirmation=bool(findings),
    )
