import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.models.base import db


class Post(db.Model):
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False)
    body: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False)
    created: Mapped[datetime] = mapped_column(sqlalchemy.DateTime, default=datetime.utcnow)
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id"))
    
    # Relação com User
    author: Mapped["User"] = relationship(backref="posts")

    def __init__(self, title: str, body: str, author_id: int):
        self.title = title
        self.body = body
        self.author_id = author_id

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r})"
