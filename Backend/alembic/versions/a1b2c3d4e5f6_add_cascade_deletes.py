"""add cascade deletes

Revision ID: a1b2c3d4e5f6
Revises: 9c1e2b3a4f5c
Create Date: 2026-05-19 06:15:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "9c1e2b3a4f5c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("routes_bus_id_fkey", "routes", type_="foreignkey")
    op.create_foreign_key(
        "routes_bus_id_fkey",
        "routes",
        "buses",
        ["bus_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.drop_constraint("schedules_bus_id_fkey", "schedules", type_="foreignkey")
    op.create_foreign_key(
        "schedules_bus_id_fkey",
        "schedules",
        "buses",
        ["bus_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.drop_constraint("schedules_route_id_fkey", "schedules", type_="foreignkey")
    op.create_foreign_key(
        "schedules_route_id_fkey",
        "schedules",
        "routes",
        ["route_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.drop_constraint("bookings_schedule_id_fkey", "bookings", type_="foreignkey")
    op.create_foreign_key(
        "bookings_schedule_id_fkey",
        "bookings",
        "schedules",
        ["schedule_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.drop_constraint("favorites_bus_id_fkey", "favorites", type_="foreignkey")
    op.create_foreign_key(
        "favorites_bus_id_fkey",
        "favorites",
        "buses",
        ["bus_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("favorites_bus_id_fkey", "favorites", type_="foreignkey")
    op.create_foreign_key(
        "favorites_bus_id_fkey",
        "favorites",
        "buses",
        ["bus_id"],
        ["id"]
    )

    op.drop_constraint("bookings_schedule_id_fkey", "bookings", type_="foreignkey")
    op.create_foreign_key(
        "bookings_schedule_id_fkey",
        "bookings",
        "schedules",
        ["schedule_id"],
        ["id"]
    )

    op.drop_constraint("schedules_route_id_fkey", "schedules", type_="foreignkey")
    op.create_foreign_key(
        "schedules_route_id_fkey",
        "schedules",
        "routes",
        ["route_id"],
        ["id"]
    )

    op.drop_constraint("schedules_bus_id_fkey", "schedules", type_="foreignkey")
    op.create_foreign_key(
        "schedules_bus_id_fkey",
        "schedules",
        "buses",
        ["bus_id"],
        ["id"]
    )

    op.drop_constraint("routes_bus_id_fkey", "routes", type_="foreignkey")
    op.create_foreign_key(
        "routes_bus_id_fkey",
        "routes",
        "buses",
        ["bus_id"],
        ["id"]
    )
