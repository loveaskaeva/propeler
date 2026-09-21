from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0)
    is_active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ServiceOut(ServiceBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ContactRequestBase(BaseModel):
    client_name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=30)
    message: Optional[str] = None
    service_id: Optional[int] = None


class ContactRequestCreate(ContactRequestBase):
    pass


class ContactRequestOut(ContactRequestBase):
    id: int
    created_at: datetime
    service: Optional[ServiceOut] = None
    model_config = ConfigDict(from_attributes=True)
