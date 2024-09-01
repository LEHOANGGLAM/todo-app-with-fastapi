"""Generate seed data

Revision ID: 14382942a71e
Revises: 73345c75a495
Create Date: 2024-08-26 20:59:26.628214

"""
from typing import Sequence, Union

from uuid import uuid4
from datetime import datetime, timezone
from alembic import op
from sqlalchemy import Table, MetaData

from schemas.user import get_password_hash
from schemas.base_entity import TaskStatus, TaskPriority, CompanyMode
from settings import ADMIN_DEFAULT_PASSWORD


# revision identifiers, used by Alembic.
revision: str = '1d8265862dda'
down_revision: Union[str, None] = 'f638f1813511'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = 'f638f1813511'


def upgrade() -> None:
    company_id_1 = uuid4()
    company_id_2 = uuid4()
    user_id_1 = uuid4()
    user_id_2 = uuid4()
    task_id_1 = uuid4()
    task_id_2 = uuid4()
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)

    meta = MetaData()

    companies = Table('companies', meta, autoload_with=op.get_bind())
    users = Table('users', meta, autoload_with=op.get_bind())
    tasks = Table('tasks', meta, autoload_with=op.get_bind())

    op.bulk_insert(
        companies,
        [
            {
                'id': company_id_1,
                'name': 'Company 1',
                'description': 'Company 1 description',
                'mode': CompanyMode.ACTIVE.name,
                'rating': 5,
                'created_at': created_at,
                'updated_at': updated_at
            },
            {
                'id': company_id_2,
                'name': 'Company 2',
                'description': 'Company 2 description',
                'mode': CompanyMode.ACTIVE.name,
                'rating': 4,
                'created_at': created_at,
                'updated_at': updated_at
            }
        ]
    )

    op.bulk_insert(
        users,
        [
            {
                'id': user_id_1,
                'email': 'admin@gmail.com',
                'username': 'admin',
                'first_name': 'Admin',
                'last_name': 'admin',
                'hashed_password': get_password_hash(ADMIN_DEFAULT_PASSWORD),
                'is_active': True,
                'is_admin': True,
                'created_at': created_at,
                'updated_at': updated_at,
                'company_id': company_id_1
            },
            {
                'id': user_id_2,
                'email': 'user@gmail.com',
                'username': 'user',
                'first_name': 'User',
                'last_name': 'user',
                'hashed_password': get_password_hash('123456'),
                'is_active': True,
                'is_admin': False,
                'created_at': created_at,
                'updated_at': updated_at,
                'company_id': company_id_2
            }
        ]
    )

    op.bulk_insert(
        tasks,
        [
            {
                'id': task_id_1,
                'summary': 'Task 1',
                'description': 'Task 1 description',
                'status': TaskStatus.IN_PROCESS.name,
                'priority': TaskPriority.CRITICAL.name,
                'user_id': user_id_1,
                'created_at': created_at,
                'updated_at': updated_at
            },
            {
                'id': task_id_2,
                'summary': 'Task 2',
                'description': 'Task 2 description',
                'status': TaskStatus.TODO.name,
                'priority': TaskPriority.MINOR.name,
                'user_id': user_id_1,
                'created_at': created_at,
                'updated_at': updated_at
            }
        ]
    )


def downgrade() -> None:
    op.execute("DELETE FROM tasks")
    op.execute("DELETE FROM users")
    op.execute("DELETE FROM companies")