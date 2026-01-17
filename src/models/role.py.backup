import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import db


class Role(db.Model):
    id: Mapped[str] = mapped_column(sqlalchemy.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")  # type: ignore

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name{self.name!r})"  # type: ignore
