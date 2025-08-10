from ..lib.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey
from typing import List


class UserApplication(db.Model):
    __tablename__ = "user_applications"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    """Application ID"""

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    """Application name"""

    deployments: Mapped[List["Deployment"]] = relationship(back_populates="user_app")


class Deployment(db.Model):
    __tablename__ = "deployments"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    """Deployment ID"""

    created_at: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    """Unix timestamp for when the deployment was created"""

    app_id: Mapped[int] = mapped_column(ForeignKey("user_applications.id"))
    """App ID for the deployment"""

    user_app: Mapped["UserApplication"] = relationship(back_populates="deployments")
