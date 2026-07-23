"""initial_core_schema

Revision ID: 7b7e422b7a8d
Revises: 
Create Date: 2026-07-23 12:42:39.870753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b7e422b7a8d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    from db.models import Base
    
    connection = op.get_bind()
    
    # Pre-create all core target schemas (excluding system)
    schemas = [
        "platform", "authz", "catalog", "astrology", "ai", "billing",
        "filestorage", "comms", "analytics", "audit"
    ]
    for schema in schemas:
        connection.execute(sa.text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        
    # Create all core tables using metadata mapping
    Base.metadata.create_all(connection)


def downgrade() -> None:
    """Downgrade schema."""
    from db.models import Base
    
    connection = op.get_bind()
    
    # Drop all core tables using metadata mapping
    Base.metadata.drop_all(connection)
    
    # Drop all core schemas
    schemas = [
        "platform", "authz", "catalog", "astrology", "ai", "billing",
        "filestorage", "comms", "analytics", "audit"
    ]
    for schema in schemas:
        connection.execute(sa.text(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))

