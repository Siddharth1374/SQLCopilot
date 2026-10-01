from pydantic import BaseModel, ConfigDict, Field

from app.schemas.schema_models import DatabaseSchema


class ParseSchemaRequest(BaseModel):
    ddl: str = Field(..., description="CREATE TABLE statements")


class NLToSQLRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    question: str
    db_schema: DatabaseSchema = Field(..., alias="schema")


class SQLToNLRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sql: str
    db_schema: DatabaseSchema | None = Field(None, alias="schema")


class ValidateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sql: str
    db_schema: DatabaseSchema = Field(..., alias="schema")


class FormatRequest(BaseModel):
    sql: str
    uppercase: bool = True


class ExecuteRequest(BaseModel):
    sql: str
    confirm_destructive: bool = False


class HistoryUpdate(BaseModel):
    name: str | None = None
    saved: bool | None = None
