from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_context, get_db_context
from models.company import ViewCompanyModel, CreateCompanyModel
from services.exception import ResourceNotFoundError, AccessDeniedError
from services import company as CompanyService
from services import auth as AuthService
from schemas import User

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("", response_model=list[ViewCompanyModel])
async def get_all_companies(async_db: AsyncSession = Depends(get_async_db_context)):
    return await CompanyService.get_companies(async_db)

@router.get("/{compapy_id}", status_code=status.HTTP_200_OK, response_model=ViewCompanyModel)
async def get_company_by_id(compapy_id: UUID, db: Session = Depends(get_async_db_context)):    
    compapy = CompanyService.get_company_by_id(db, compapy_id)
    if compapy is None:
        raise ResourceNotFoundError()
    return compapy

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ViewCompanyModel)
async def create_company(request: CreateCompanyModel,  db: Session = Depends(get_db_context)):
    return CompanyService.create_company(db, request)

@router.put("/{compapy_id}", status_code=status.HTTP_200_OK, response_model=ViewCompanyModel)
async def update_company(
    compapy_id: UUID,
    request: CreateCompanyModel,
    db: Session = Depends(get_db_context),
    ):
        return CompanyService.update_company(db, compapy_id, request)

@router.delete("/{compapy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(compapy_id: UUID, db: Session = Depends(get_db_context)):
    CompanyService.delete_company(db, compapy_id)
    
    
#delete if user = admin or 

# @router.post("", status_code=status.HTTP_201_CREATED, response_model=BookViewModel)
# async def create_book(
#     request: BookModel, 
#     user: User = Depends(AuthService.token_interceptor),
#     db: Session = Depends(get_db_context),
#     ):
#         if not user:
#             raise AccessDeniedError()
        
#         request.owner_id = user.id

#         return BookService.add_new_book(db, request)