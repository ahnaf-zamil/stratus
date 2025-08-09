from ..lib.db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger

class UserApplication(db.Model):
    __tablename__ = "user_applications"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
