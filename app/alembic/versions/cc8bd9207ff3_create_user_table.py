"""create user table

Revision ID: 726914b39918
Revises: ca1cfdb3e8b0
Create Date: 2024-09-01 18:43:53.362835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc8bd9207ff3'
down_revision: Union[str, None] = '79a8bad94c4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = '79a8bad94c4a'


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_admin', sa.Boolean, default=False),
        sa.Column('company_id', sa.UUID, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_foreign_key('fk_user_company', 'users', 'companies', ['company_id'], ['id'])

def downgrade() -> None:
    op.drop_table('users')
