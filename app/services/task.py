from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from services import utils
from models import CreateTaskModel
from schemas import Task
from services.exception import ResourceNotFoundError


async def get_tasks(async_db: AsyncSession) -> list[Task]:
    result = await async_db.scalars(select(Task).order_by(Task.created_at))
    return result.all()

def get_task_by_id(db: Session, task_id: UUID) -> Task:
    return db.scalars(select(Task).filter(Task.id == task_id)).first()

def create_task(db: Session, data: CreateTaskModel) -> Task:
    task = Task(**data.model_dump())
    task.created_at = utils.get_current_utc_time()
    task.updated_at = utils.get_current_utc_time()
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, id: UUID, data: CreateTaskModel) -> Task:
    task = get_task_by_id(db, id)
    if task is None:
        raise ResourceNotFoundError()
    
    task.summary = data.summary
    task.description = data.description
    task.status = data.status
    task.priority = data.priority
    task.user_id = data.user_id
    task.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, id: UUID) -> None:
    task = get_task_by_id(db, id)
    if task is None:
        raise ResourceNotFoundError()
    
    db.delete(task)
    db.commit()
    