from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_context, get_db_context
from models.company import ViewCompanyModel, CreateCompanyModel, SearchCompanyModel
from services.exception import ResourceNotFoundError
from services import company as CompanyService
from schemas import CompanyMode

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("", response_model=list[ViewCompanyModel])
async def get_all_companies(
    name: str = Query(default=None),
    mode: CompanyMode = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10), async_db: AsyncSession = Depends(get_async_db_context)):
    conds = SearchCompanyModel(name, mode, page, size)
    return await CompanyService.get_companies(conds, async_db)

@router.get("/{compapy_id}", status_code=status.HTTP_200_OK, response_model=ViewCompanyModel)
async def get_company_by_id(compapy_id: UUID, db: Session = Depends(get_async_db_context)):    
    compapy = CompanyService.get_company_by_id(db, compapy_id)
    if compapy is None:
        raise ResourceNotFoundError()
    return compapy

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ViewCompanyModel)
def create_company(request: CreateCompanyModel,  db: Session = Depends(get_db_context)):
    return CompanyService.create_company(db, request)

@router.put("/{compapy_id}", status_code=status.HTTP_200_OK, response_model=ViewCompanyModel)
def update_company(
    compapy_id: UUID,
    request: CreateCompanyModel,
    db: Session = Depends(get_db_context),
    ):
        return CompanyService.update_company(db, compapy_id, request)

@router.delete("/{compapy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(compapy_id: UUID, db: Session = Depends(get_db_context)):
    CompanyService.delete_company(db, compapy_id)
    
    