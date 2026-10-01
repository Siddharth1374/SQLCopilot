from fastapi import APIRouter, HTTPException

from app.schemas.requests import ParseSchemaRequest
from app.schemas.schema_models import DatabaseSchema
from app.services.schema_service import parse_ddl

router = APIRouter(prefix="/schema", tags=["schema"])


@router.post("/parse", response_model=DatabaseSchema)
def parse_schema(req: ParseSchemaRequest):
    try:
        schema = parse_ddl(req.ddl)
    except Exception as e:
        raise HTTPException(400, f"Could not parse schema: {e}")
    if not schema.tables:
        raise HTTPException(400, "No CREATE TABLE statements found")
    return schema
