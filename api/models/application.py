"""
SQLAlchemy models for user applications and their deployments.
Defines relationships and schema for persistence.
"""

from typing import List

from sqlalchemy import String, BigInteger, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..lib.runtimes import get_runtime_by_id
from .common import TimestampModel


class UserApplication(TimestampModel):
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

    current_deployment_id: Mapped[str] = mapped_column(
        String(32), nullable=True
    )  # Initially an application won't have deployments
    """ID of the currently running deployment"""

    git_repo: Mapped[str] = mapped_column(Text(), nullable=False)
    """Remote Git repo URL to fetch application code"""

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "runtime": get_runtime_by_id(self.runtime),
            "current_deployment_id": self.current_deployment_id,
            "git_repo": self.git_repo,
            "created_at": int(self.created_at.timestamp()),
        }


class Deployment(TimestampModel):
    __tablename__ = "deployments"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    """Unique deployment ID (UUID or hash)"""

    app_id: Mapped[int] = mapped_column(
        ForeignKey("user_applications.id", ondelete="CASCADE"), nullable=False
    )
    """Foreign key to the associated application"""

    user_app: Mapped["UserApplication"] = relationship(back_populates="deployments")
    """Reference to the parent application"""

    def to_json(self):
        return {"id": self.id, "created_at": int(self.created_at.timestamp())}
