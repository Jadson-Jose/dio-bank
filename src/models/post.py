
from datetime import datetime
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import db


class Post(db.Model):
    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False)
    body: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False)
    created: Mapped[datetime] = mapped_column(sqlalchemy.DateTime, default=datetime.now)
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"))

    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body

    def __repr__(self) -> str:
        return (
            f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"
        )