from sqlalchemy.orm import Session

from app.db.models import HistoryItem


def add(db: Session, **kw) -> HistoryItem:
    item = HistoryItem(**kw)
    db.add(item); db.commit(); db.refresh(item)
    return item


def list_all(db: Session, saved_only: bool = False) -> list[HistoryItem]:
    q = db.query(HistoryItem)
    if saved_only:
        q = q.filter(HistoryItem.saved.is_(True))
    return q.order_by(HistoryItem.created_at.desc()).limit(100).all()


def update(db: Session, item_id: int, name: str | None, saved: bool | None) -> HistoryItem | None:
    item = db.get(HistoryItem, item_id)
    if not item:
        return None
    if name is not None:
        item.name = name
    if saved is not None:
        item.saved = saved
    db.commit(); db.refresh(item)
    return item


def delete(db: Session, item_id: int) -> bool:
    item = db.get(HistoryItem, item_id)
    if not item:
        return False
    db.delete(item); db.commit()
    return True
