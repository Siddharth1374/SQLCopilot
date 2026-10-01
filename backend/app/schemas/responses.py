from datetime import datetime

from pydantic import BaseModel


class Check(BaseModel):
    label: str
    ok: bool


class ValidationResult(BaseModel):
    valid: bool
    checks: list[Check]
    errors: list[str] = []


class SafetyReport(BaseModel):
    safe: bool
    risk_level: str  # none | low | high
    findings: list[str]
    requires_confirmation: bool


class NLToSQLResponse(BaseModel):
    sql: str
    validation: ValidationResult
    safety: SafetyReport
    explanation: str
    optimizations: list[str]


class SQLToNLResponse(BaseModel):
    explanation: str
    steps: list[str]
    optimizations: list[str]


class HistoryOut(BaseModel):
    id: int
    name: str
    natural_language: str
    sql: str
    direction: str
    saved: bool
    created_at: datetime

    model_config = {"from_attributes": True}
