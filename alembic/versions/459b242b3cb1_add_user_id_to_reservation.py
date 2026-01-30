"""Add user_id to reservation

Revision ID: 459b242b3cb1
Revises: d6f6da62e1fc
Create Date: 2026-01-30 17:54:51.258828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '459b242b3cb1'
down_revision: Union[str, None] = 'd6f6da62e1fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_reservation_user_id_user', 'user', ['user_id'], ['id']
        )


def downgrade() -> None:
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_constraint('fk_reservation_user_id_user', type_='foreignkey')
        batch_op.drop_column('user_id')
