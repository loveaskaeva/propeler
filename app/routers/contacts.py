from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/contact-requests", tags=["contact-requests"])


@router.post("", response_model=schemas.ContactRequestOut, status_code=status.HTTP_201_CREATED)
def create_contact(data: schemas.ContactRequestCreate, db: Session = Depends(get_db)):
    return crud.create_contact_request(db, data)


@router.get("", response_model=List[schemas.ContactRequestOut])
def get_contacts(service_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.list_contact_requests(db, service_id=service_id)
