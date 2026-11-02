"""add event user foreign key

Revision ID: 01edefbac55b
Revises:
Create Date: 2026-09-20 13:07:07.231597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01edefbac55b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        'events',
        'user_id',
        existing_type=sa.INTEGER(),
        nullable=False
    )

    op.create_foreign_key(
        'fk_events_user_id_users',
        'events',
        'users',
        ['user_id'],
        ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        'fk_events_user_id_users',
        'events',
        type_='foreignkey'
    )

    op.alter_column(
        'events',
        'user_id',
        existing_type=sa.INTEGER(),
        nullable=True
    )