from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=List[schemas.ServiceOut])
def get_services(only_active: bool = True, db: Session = Depends(get_db)):
    return crud.list_services(db, only_active=only_active)


@router.post("", response_model=schemas.ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(data: schemas.ServiceCreate, db: Session = Depends(get_db)):
    return crud.create_service(db, data)


@router.get("/{service_id}", response_model=schemas.ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    obj = crud.get_service(db, service_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return obj


@router.patch("/{service_id}", response_model=schemas.ServiceOut)
def update_service(service_id: int, data: schemas.ServiceUpdate, db: Session = Depends(get_db)):
    obj = crud.update_service(db, service_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
    return obj
