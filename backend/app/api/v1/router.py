from fastapi import APIRouter

from app.api.v1.routes import execute, health, history, schema, translate

api_router = APIRouter()
for r in (health.router, schema.router, translate.router, execute.router, history.router):
    api_router.include_router(r)
