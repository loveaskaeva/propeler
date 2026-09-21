from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, schemas


def get_service(db: Session, service_id: int) -> Optional[models.Service]:
    return db.query(models.Service).filter(models.Service.id == service_id).first()


def list_services(db: Session, only_active: bool = True) -> List[models.Service]:
    q = db.query(models.Service)
    if only_active:
        q = q.filter(models.Service.is_active.is_(True))
    return q.order_by(models.Service.id).all()


def create_service(db: Session, data: schemas.ServiceCreate) -> models.Service:
    obj = models.Service(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_service(db: Session, service_id: int, data: schemas.ServiceUpdate) -> Optional[models.Service]:
    obj = get_service(db, service_id)
    if not obj:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def create_contact_request(db: Session, data: schemas.ContactRequestCreate) -> models.ContactRequest:
    obj = models.ContactRequest(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_contact_requests(db: Session, service_id: Optional[int] = None) -> List[models.ContactRequest]:
    q = db.query(models.ContactRequest)
    if service_id:
        q = q.filter(models.ContactRequest.service_id == service_id)
    return q.order_by(models.ContactRequest.created_at.desc()).all()
