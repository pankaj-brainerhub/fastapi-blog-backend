"""seed default roles

Revision ID: 4ce2f323dbb3
Revises: 765ae22a0637
Create Date: 2026-08-11 12:36:53.286716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ce2f323dbb3'
down_revision: Union[str, Sequence[str], None] = '765ae22a0637'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    roles_table = sa.table(
        "roles",
        sa.column("id", sa.String(length=20)),
        sa.column("name", sa.String(length=50)),
    )

    op.bulk_insert(
        roles_table,
        [
            {
                "id": "ADMIN",
                "name": "admin",
            },
            {
                "id": "USER",
                "name": "user",
            },
        ],
    )


def downgrade() -> None:
    roles_table = sa.table(
        "roles",
        sa.column("id", sa.String(length=20)),
        sa.column("name", sa.String(length=50)),
    )

    op.execute(
        roles_table.delete().where(
            roles_table.c.id.in_(["ADMIN", "USER"])
        )
    )
