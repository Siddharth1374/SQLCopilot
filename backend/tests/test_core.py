from app.services import optimizer, safety, sql_parser, validator
from app.services.schema_service import parse_ddl

DDL = open("../scripts/demo_schema.sql").read()
SCHEMA = parse_ddl(DDL)


def test_schema_parsing():
    assert {"employees", "departments", "users", "orders"} <= SCHEMA.table_names()
    emp = next(t for t in SCHEMA.tables if t.name == "employees")
    assert any(c.references == "departments.id" for c in emp.columns)


def test_validator_ok():
    r = validator.validate("SELECT * FROM employees WHERE salary > 50000", SCHEMA)
    assert r.valid


def test_validator_unknown_column():
    r = validator.validate("SELECT bonus FROM employees", SCHEMA)
    assert not r.valid


def test_safety_blocks_delete_without_where():
    r = safety.analyze("DELETE FROM employees", read_only=False)
    assert r.risk_level == "high" and r.requires_confirmation


def test_safety_select_is_safe():
    assert safety.analyze("SELECT 1").safe


def test_optimizer_join_index():
    sql = "SELECT d.name, COUNT(e.id) FROM departments d JOIN employees e ON d.id = e.department_id GROUP BY d.name"
    assert any("department_id" in t for t in optimizer.suggest(sql))


def test_ir():
    ir = sql_parser.build_ir(sql_parser.parse("SELECT name FROM users WHERE id = 1 LIMIT 5"))
    assert ir["limit"] == "5" and ir["where"]


def test_api_flow():
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as c:
        assert c.get("/api/v1/health").status_code == 200
        r = c.post("/api/v1/sql-to-nl", json={"sql": "SELECT name FROM users WHERE id = 1"})
        assert r.status_code == 200 and r.json()["steps"]
        assert len(c.get("/api/v1/history").json()) >= 1
