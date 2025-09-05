"""
SQLAlchemy models for user applications and their deployments.
Defines relationships and schema for persistence.
"""

from typing import List

from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..lib.db import db


class UserApplication(db.Model):
    __tablename__ = "user_applications"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=True)
    """Primary key for the application"""

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    """Human-readable name of the application"""

    runtime: Mapped[str] = mapped_column(String(30), nullable=False)
    """Runtime environment (e.g. Python, Node)"""

    deployments: Mapped[List["Deployment"]] = relationship(
        back_populates="user_app",
        cascade="all, delete-orphan",  # Automatically delete deployments when app is deleted
    )
    """One-to-many relationship with deployments"""


class Deployment(db.Model):
    __tablename__ = "deployments"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    """Unique deployment ID (UUID or hash)"""

    created_at: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    """Unix timestamp of deployment creation"""

    app_id: Mapped[int] = mapped_column(
        ForeignKey("user_applications.id", ondelete="CASCADE"), nullable=False
    )
    """Foreign key to the associated application"""

    user_app: Mapped["UserApplication"] = relationship(back_populates="deployments")
    """Reference to the parent application"""
