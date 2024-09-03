from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from services import utils
from models import CreateUserModel, SearchUserModel
from schemas import User
from services.exception import ResourceNotFoundError


async def get_users(conds: SearchUserModel, async_db: AsyncSession) -> list[User]:
    query = select(User).order_by(User.created_at)
    
    if conds.email is not None:
        query = query.filter(User.email.like(f"%{conds.email}%"))
    if conds.username is not None:
        query = query.filter(User.username.like(f"%{conds.username}%"))
    if conds.first_name is not None:
        query = query.filter(User.first_name.like(f"%{conds.first_name}%"))  
    if conds.last_name is not None:
        query = query.filter(User.last_name.like(f"%{conds.last_name}%"))                        
    if conds.is_active is not None:
        query = query.filter(User.is_active == conds.is_active) 
    
    query = query.offset((conds.page - 1) * conds.size).limit(conds.size)
    
    result = await async_db.scalars(query)
    return result.all()

def get_user_by_id(db: Session, user_id: UUID) -> User:
    return db.scalars(select(User).filter(User.id == user_id)).first()

def create_user(db: Session, data: CreateUserModel) -> User:
    user = User(**data.model_dump())
    user.created_at = utils.get_current_utc_time()
    user.updated_at = utils.get_current_utc_time()
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, id: UUID, data: CreateUserModel) -> User:
    user = get_user_by_id(db, id)
    if user is None:
        raise ResourceNotFoundError()
    
    user.email = data.email
    user.username = data.username
    user.hashed_password = data.hashed_password
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.is_active = data.is_active
    user.is_admin = data.is_admin
    user.company_id = data.company_id
    user.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, id: UUID) -> None:
    user = get_user_by_id(db, id)
    if user is None:
        raise ResourceNotFoundError()
    
    db.delete(user)
    db.commit()
    