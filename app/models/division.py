import uuid

from sqlalchemy import Column, Numeric, TIMESTAMP, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from app.core.config_db import Base

    
class Division(Base):
    __tablename__ = "division"

    division_practice_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    questions = Column(
        JSONB,
        nullable=False
    )

    score = Column(
        String(20),
        nullable=True
    )

    total_time_taken = Column(
        Numeric(10, 2),
        nullable=True
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )