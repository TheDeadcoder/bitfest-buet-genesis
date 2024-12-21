from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# class Organization(Base):
#     __tablename__ = "organizations"
    
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String, nullable=False)
#     about = Column(String, nullable=True)
#     location = Column(String, nullable=True)
#     country = Column(String, nullable=True)
#     image_link = Column(String, nullable=True)
    
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class OrganizationBase(BaseModel):
    name: str
    about: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    image_link: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    pass

class OrganizationInDBBase(OrganizationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

