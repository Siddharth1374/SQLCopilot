from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.schemas.requests import ExecuteRequest
from app.services import safety
from app.services.executor import execute_readonly

router = APIRouter(prefix="/execute", tags=["execute"])


@router.post("")
def execute(req: ExecuteRequest):
    report = safety.analyze(req.sql, settings.read_only_mode)
    if settings.read_only_mode and report.risk_level == "high":
        raise HTTPException(403, {"message": "Blocked by read-only mode", "findings": report.findings})
    if report.requires_confirmation and not req.confirm_destructive:
        raise HTTPException(409, {"message": "Confirmation required", "findings": report.findings})
    try:
        return execute_readonly(req.sql)
    except Exception as e:
        raise HTTPException(400, str(e))
