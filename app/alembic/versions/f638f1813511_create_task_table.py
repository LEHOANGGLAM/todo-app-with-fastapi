"""create task  table

Revision ID: 4dcd409af7ba
Revises: 726914b39918
Create Date: 2024-09-01 18:44:05.934385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from schemas import TaskPriority,TaskStatus


# revision identifiers, used by Alembic.
revision: str = 'f638f1813511'
down_revision: Union[str, None] = 'cc8bd9207ff3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = 'cc8bd9207ff3'


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('description', sa.String),
        sa.Column('summary', sa.String, nullable=False),
        sa.Column('status', sa.Enum(TaskStatus), nullable=False, default=TaskStatus.TODO),
        sa.Column('priority', sa.Enum(TaskPriority), nullable=False, default=TaskPriority.MINOR),
        sa.Column('user_id', sa.UUID, nullable=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_foreign_key('fk_task_user', 'tasks', 'users', ['user_id'], ['id'])
    op.create_index("idx_task_summary_prio_status", "tasks", ["summary", "priority", "status"])

def downgrade() -> None:
    op.drop_table('tasks')
    op.execute('DROP TYPE taskstatus;')
    op.execute('DROP TYPE taskpriority;')