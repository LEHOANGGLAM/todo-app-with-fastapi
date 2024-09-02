from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_context, get_db_context
from models.task import ViewTaskModel, CreateTaskModel
from services.exception import ResourceNotFoundError, AccessDeniedError
from services import task as TaskService
from services import auth as AuthService
from schemas import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=list[ViewTaskModel])
def get_all_tasks(db: Session = Depends(get_db_context), user: User = Depends(AuthService.token_interceptor)):    
    return TaskService.get_tasks(db, user, joined_load=True)

@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=ViewTaskModel)
def get_task_by_id(task_id: UUID, db: Session = Depends(get_db_context), user: User = Depends(AuthService.token_interceptor)):    
    task = TaskService.get_task_by_id(db, task_id, user, joined_load=True)
    if task is None:
        raise ResourceNotFoundError()
    return task

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ViewTaskModel)
def create_task(request: CreateTaskModel,  db: Session = Depends(get_db_context)):
    return TaskService.create_task(db, request)

@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=ViewTaskModel)
async def update_task(
    task_id: UUID,
    request: CreateTaskModel,
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor)
    ):
        return TaskService.update_task(db, task_id, request, user)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, db: Session = Depends(get_db_context), user: User = Depends(AuthService.token_interceptor)):
    TaskService.delete_task(db, task_id, user)
    