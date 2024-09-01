from database import Base
from sqlalchemy import Column, String, Enum, SmallInteger
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity, CompanyMode

class Company(Base, BaseEntity):
    __tablename__ = "companies"

    name = Column(String, nullable=False)
    description = Column(String)
    mode = Column(Enum(CompanyMode), nullable=False, default=CompanyMode.UNKNOWN)
    rating = Column(SmallInteger, nullable=False, default=0)
    
    users = relationship("User", back_populates="company")