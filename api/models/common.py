"""
Shared SQLAlchemy models
These are to be implemented or extended by models in other files
"""

from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column

from ..lib.db import db


class TimestampModel(db.Model):
    """This base model must be inherited by all models requiring 'created_at' and 'updated_at' columns"""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
