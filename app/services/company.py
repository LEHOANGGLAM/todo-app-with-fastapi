from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from services import utils
from models import CreateCompanyModel, SearchCompanyModel
from schemas import Company
from services.exception import ResourceNotFoundError


async def get_companies(conds: SearchCompanyModel, async_db: AsyncSession) -> list[Company]:
    query = select(Company).order_by(Company.created_at)
    
    if conds.name is not None:
        query = query.filter(Company.name.like(f"%{conds.name}%"))
    if conds.mode is not None:
        query = query.filter(Company.mode == conds.mode)
    
    query = query.offset((conds.page - 1) * conds.size).limit(conds.size)
    
    result = await async_db.scalars(query)
    return result.all()

def get_company_by_id(db: Session, compapy_id: UUID) -> Company:
    return db.scalars(select(Company).filter(Company.id == compapy_id)).first()

def create_company(db: Session, data: CreateCompanyModel) -> Company:
    company = Company(**data.model_dump())
    company.created_at = utils.get_current_utc_time()
    company.updated_at = utils.get_current_utc_time()
    
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

def update_company(db: Session, id: UUID, data: CreateCompanyModel) -> Company:
    company = get_company_by_id(db, id)
    if company is None:
        raise ResourceNotFoundError()
    
    company.name = data.name
    company.description = data.description
    company.mode = data.mode
    company.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(company)
    return company

def delete_company(db: Session, id: UUID) -> None:
    company = get_company_by_id(db, id)
    if company is None:
        raise ResourceNotFoundError()
    
    db.delete(company)
    db.commit()
    