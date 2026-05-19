"""change ids to int

Revision ID: 9c1e2b3a4f5c
Revises: f6f60c3d5988
Create Date: 2026-05-18 10:59:30.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "9c1e2b3a4f5c"
down_revision: Union[str, Sequence[str], None] = "f6f60c3d5988"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop dependent tables first due to foreign keys.
    op.drop_table("bookings")
    op.drop_table("schedules")
    op.drop_table("routes")
    op.drop_table("favorites")
    op.drop_table("buses")

    # Recreate buses with integer PK and integer FKs from routes/schedules.
    op.create_table(
        "buses",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("owner_id", postgresql.UUID(), nullable=True),
        sa.Column("bus_name", sa.String(), nullable=False),
        sa.Column("bus_number", sa.String(), nullable=False),
        sa.Column("bus_type", sa.String(), nullable=True),
        sa.Column("total_seats", sa.Integer(), nullable=False),
        sa.Column("operator_name", sa.String(), nullable=True),
        sa.Column("amenities", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.UniqueConstraint("bus_number")
    )

    op.create_table(
        "favorites",
        sa.Column("id", postgresql.UUID(), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(), nullable=True),
        sa.Column("bus_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["bus_id"], ["buses.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"])
    )

    op.create_table(
        "routes",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("bus_id", sa.Integer(), nullable=True),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("destination", sa.String(), nullable=False),
        sa.Column("distance", sa.Float(), nullable=True),
        sa.Column("duration", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["bus_id"], ["buses.id"])
    )

    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("bus_id", sa.Integer(), nullable=True),
        sa.Column("route_id", sa.Integer(), nullable=True),
        sa.Column("departure_time", sa.DateTime(), nullable=True),
        sa.Column("arrival_time", sa.DateTime(), nullable=True),
        sa.Column("journey_date", sa.Date(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("available_seats", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["bus_id"], ["buses.id"]),
        sa.ForeignKeyConstraint(["route_id"], ["routes.id"])
    )

    op.create_table(
        "bookings",
        sa.Column("id", postgresql.UUID(), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(), nullable=True),
        sa.Column("schedule_id", sa.Integer(), nullable=True),
        sa.Column("seat_number", sa.String(), nullable=False),
        sa.Column("booking_status", sa.String(), nullable=True),
        sa.Column("booking_date", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["schedule_id"], ["schedules.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"])
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("bookings")
    op.drop_table("schedules")
    op.drop_table("routes")
    op.drop_table("favorites")
    op.drop_table("buses")
