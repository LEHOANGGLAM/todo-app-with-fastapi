from database import Base
from sqlalchemy import Column, String, Boolean, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"])

class User(Base, BaseEntity):
    __tablename__ = "users"

    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=False)
    
    company = relationship("Company")
    
def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hased_password):
    return bcrypt_context.verify(plain_password, hased_password)
