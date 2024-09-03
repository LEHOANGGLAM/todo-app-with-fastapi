from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_context, get_db_context
from models.user import ViewUserModel, CreateUserModel, SearchUserModel
from services.exception import ResourceNotFoundError
from services import user as UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[ViewUserModel])
async def get_all_users(
    email: str = Query(default=None),
    username: str = Query(default=None),
    first_name: str = Query(default=None),
    last_name: str = Query(default=None),
    is_active: bool = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    async_db: AsyncSession = Depends(get_async_db_context)):
    conds = SearchUserModel(email, username, first_name, last_name, is_active, page, size)
    return await UserService.get_users(conds, async_db)

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=ViewUserModel)
async def get_user_by_id(user_id: UUID, db: Session = Depends(get_async_db_context)):    
    user = UserService.get_user_by_id(db, user_id)
    if user is None:
        raise ResourceNotFoundError()
    return user

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ViewUserModel)
async def create_user(request: CreateUserModel,  db: Session = Depends(get_db_context)):
    return UserService.create_user(db, request)

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=ViewUserModel)
async def update_user(
    user_id: UUID,
    request: CreateUserModel,
    db: Session = Depends(get_db_context),
    ):
        return UserService.update_user(db, user_id, request)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: Session = Depends(get_db_context)):
    UserService.delete_user(db, user_id)
    