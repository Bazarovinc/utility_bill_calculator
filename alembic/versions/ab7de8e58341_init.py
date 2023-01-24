"""init

Revision ID: ab7de8e58341
Revises: 
Create Date: 2023-01-06 21:14:33.262917

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "ab7de8e58341"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "measurements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("month", sa.Integer(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("cold_measurement", sa.DECIMAL(precision=8, scale=3), nullable=True),
        sa.Column("hot_measurement", sa.DECIMAL(precision=8, scale=3), nullable=True),
        sa.Column("electricity_measurement", sa.DECIMAL(precision=8, scale=2), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cold_measurement"),
        sa.UniqueConstraint("electricity_measurement"),
        sa.UniqueConstraint("hot_measurement"),
    )
    op.create_index(op.f("ix_measurements_month"), "measurements", ["month"], unique=False)
    op.create_index(op.f("ix_measurements_year"), "measurements", ["year"], unique=False)
    op.create_table(
        "tariffs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cold_tariff", sa.DECIMAL(precision=6, scale=2), nullable=True),
        sa.Column("hot_tariff", sa.DECIMAL(precision=6, scale=2), nullable=True),
        sa.Column("electricity_tariff", sa.DECIMAL(precision=6, scale=2), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tariffs")
    op.drop_index(op.f("ix_measurements_year"), table_name="measurements")
    op.drop_index(op.f("ix_measurements_month"), table_name="measurements")
    op.drop_table("measurements")
    # ### end Alembic commands ###
