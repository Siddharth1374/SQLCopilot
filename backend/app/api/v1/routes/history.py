from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.requests import HistoryUpdate
from app.schemas.responses import HistoryOut
from app.services import history_service

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=list[HistoryOut])
def list_history(saved_only: bool = False, db: Session = Depends(get_db)):
    return history_service.list_all(db, saved_only)


@router.patch("/{item_id}", response_model=HistoryOut)
def update_item(item_id: int, body: HistoryUpdate, db: Session = Depends(get_db)):
    item = history_service.update(db, item_id, body.name, body.saved)
    if not item:
        raise HTTPException(404, "Not found")
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    if not history_service.delete(db, item_id):
        raise HTTPException(404, "Not found")
