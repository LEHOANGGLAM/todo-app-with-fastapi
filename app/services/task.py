from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from services import utils
from models import CreateTaskModel
from schemas import Task, User
from services.exception import ResourceNotFoundError
from services.user import get_user_by_id


def get_tasks(db: Session, user: User, /, joined_load = False) -> list[Task]:
    if user.is_admin is False:
        return get_tasks_by_user(db, user, joined_load)
    return db.scalars(select(Task).order_by(Task.created_at)).all()  

def get_tasks_by_user(db: Session, user: User, /, joined_load = False) -> list[Task]:   
    query = select(Task).filter(Task.user_id == user.id)
    if joined_load:
        query.options(joinedload(Task.user, innerjoin=True))  
    return db.scalars(query).all() 

def get_task_by_id(db: Session, task_id: UUID, user: User, /, joined_load = False) -> Task:
    if user.is_admin is True:
        query = select(Task).filter(Task.id == task_id).order_by(Task.created_at)
    else:
        query = select(Task).filter(Task.id == task_id, Task.user_id == user.id).order_by(Task.created_at)
    
    if joined_load:
        query.options(joinedload(Task.user, innerjoin=True))
    
    return db.scalars(query).first()

def create_task(db: Session, data: CreateTaskModel) -> Task:
    task = Task(**data.model_dump())
    task.created_at = utils.get_current_utc_time()
    task.updated_at = utils.get_current_utc_time()
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task_id: UUID, data: CreateTaskModel, user: User) -> Task:
    task = get_task_by_id(db, task_id, user)
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

def delete_task(db: Session, id: UUID, user: User) -> None:
    task = get_task_by_id(db, id, user)
    if task is None:
        raise ResourceNotFoundError()
    
    db.delete(task)
    db.commit()
        