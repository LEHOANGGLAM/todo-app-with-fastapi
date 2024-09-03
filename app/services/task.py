from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from services import utils
from models import CreateTaskModel, SearchTaskModel
from schemas import Task, User
from services.exception import ResourceNotFoundError


def get_tasks(conds: SearchTaskModel, user: User, db: Session, /, joined_load=False) -> list[Task]:
    # Start building the base query
    query = select(Task).order_by(Task.created_at)
    
    # Apply filters based on conds
    if conds.summary is not None:
        query = query.filter(Task.summary.like(f"%{conds.summary}%"))
    if conds.status is not None:
        query = query.filter(Task.status == conds.status)
    if conds.priority is not None:
        query = query.filter(Task.priority == conds.priority)
    
    # Apply user-specific filter if the user is not an admin
    if not user.is_admin:
        query = query.filter(Task.user_id == user.id)
    
    # Apply joined load if necessary
    if joined_load:
        query = query.options(joinedload(Task.user, innerjoin=True))
    
    # Apply pagination
    query = query.offset((conds.page - 1) * conds.size).limit(conds.size)
    
    # Execute the query and return the results
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
        