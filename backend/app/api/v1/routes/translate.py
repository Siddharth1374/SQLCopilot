from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.schemas.requests import FormatRequest, NLToSQLRequest, SQLToNLRequest, ValidateRequest
from app.schemas.responses import NLToSQLResponse, SQLToNLResponse, ValidationResult
from app.services import explainer, history_service, optimizer, safety, sql_parser, validator
from app.services.formatter import format_sql
from app.services.llm_service import llm_service

router = APIRouter(tags=["translate"])


@router.post("/nl-to-sql", response_model=NLToSQLResponse)
def nl_to_sql(req: NLToSQLRequest, db: Session = Depends(get_db)):
    try:
        sql = llm_service.generate_sql(req.question, req.db_schema)
    except RuntimeError as e:
        raise HTTPException(503, str(e))
    if "CANNOT_ANSWER" in sql:
        raise HTTPException(422, "The question cannot be answered with the provided schema")

    validation = validator.validate(sql, req.db_schema)
    safety_report = safety.analyze(sql, settings.read_only_mode)
    explanation, tips = "", []
    if validation.valid:
        ir = sql_parser.build_ir(sql_parser.parse(sql))
        try:
            explanation = llm_service.summarize(sql, ir)
        except RuntimeError:
            explanation = " ".join(explainer.steps_from_ir(ir))
        tips = optimizer.suggest(sql, req.db_schema)
    history_service.add(db, natural_language=req.question, sql=sql, direction="nl_to_sql")
    return NLToSQLResponse(sql=sql, validation=validation, safety=safety_report, explanation=explanation, optimizations=tips)


@router.post("/sql-to-nl", response_model=SQLToNLResponse)
def sql_to_nl(req: SQLToNLRequest, db: Session = Depends(get_db)):
    try:
        tree = sql_parser.parse(req.sql)
    except sql_parser.SQLParseError as e:
        raise HTTPException(400, f"Invalid SQL: {e}")
    ir = sql_parser.build_ir(tree)
    steps = explainer.steps_from_ir(ir)
    try:
        summary = llm_service.summarize(req.sql, ir)
    except RuntimeError:
        summary = steps[-1] if steps else ""
    history_service.add(db, natural_language=summary, sql=req.sql, direction="sql_to_nl")
    return SQLToNLResponse(explanation=summary, steps=steps, optimizations=optimizer.suggest(req.sql, req.db_schema))


@router.post("/validate", response_model=ValidationResult)
def validate_sql(req: ValidateRequest):
    return validator.validate(req.sql, req.db_schema)


@router.post("/format")
def format_endpoint(req: FormatRequest):
    try:
        return {"sql": format_sql(req.sql, req.uppercase)}
    except Exception as e:
        raise HTTPException(400, str(e))
