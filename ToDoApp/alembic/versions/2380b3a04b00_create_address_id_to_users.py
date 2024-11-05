"""Create address_id to users

Revision ID: 2380b3a04b00
Revises: 62e313ab7967
Create Date: 2024-11-05 08:01:38.752563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2380b3a04b00'
down_revision: Union[str, None] = '62e313ab7967'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        "address_users_fk", 'users', 'address', ['address_id'], ['id'], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("address_users_fk", 'users', type_='foreignkey')
    op.drop_column("users", "address_id")
