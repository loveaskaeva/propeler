from sqlalchemy import Column, String, JSON, Enum as SQLEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from .enums import JobType, JobStatus

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(SQLEnum(JobType), nullable=False)
    status = Column(SQLEnum(JobStatus), nullable=False, default=JobStatus.PENDING)
    payload = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
