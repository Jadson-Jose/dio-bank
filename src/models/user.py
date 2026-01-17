import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import db


class User(db.Model):
    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        sqlalchemy.String, unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="user")  # type: ignore
    active: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=True)

    def __init__(self, username: str, password: str, role_id: int):
        self.username = username
        self.password = password
        self.role_id = role_id

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"
        )
