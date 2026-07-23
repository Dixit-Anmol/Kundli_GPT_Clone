"""initial_schema

Revision ID: 763a1349fb03
Revises: 
Create Date: 2026-07-23 12:32:25.964190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '763a1349fb03'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    from db.models import Base
    
    connection = op.get_bind()
    
    # Pre-create all target schemas
    schemas = [
        "platform", "authz", "catalog", "astrology", "ai", "billing",
        "storage", "comms", "analytics", "audit", "system"
    ]
    for schema in schemas:
        connection.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        
    # Create all tables using metadata mapping
    Base.metadata.create_all(connection)


def downgrade() -> None:
    """Downgrade schema."""
    from db.models import Base
    
    connection = op.get_bind()
    
    # Drop all tables using metadata mapping
    Base.metadata.drop_all(connection)
    
    # Drop all schemas
    schemas = [
        "platform", "authz", "catalog", "astrology", "ai", "billing",
        "storage", "comms", "analytics", "audit", "system"
    ]
    for schema in schemas:
        connection.execute(sa.text(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))

