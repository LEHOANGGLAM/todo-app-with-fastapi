"""create company table

Revision ID: ca1cfdb3e8b0
Revises: 
Create Date: 2024-09-01 15:44:26.228851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from schemas import CompanyMode


# revision identifiers, used by Alembic.
revision: str = '79a8bad94c4a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'companies',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('mode', sa.Enum(CompanyMode), nullable=False, default=CompanyMode.UNKNOWN),
        sa.Column('rating', sa.SmallInteger, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('companies')
    op.execute("DROP TYPE companymode;")
