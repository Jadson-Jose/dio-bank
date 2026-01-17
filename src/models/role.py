import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import db


class Role(db.Model):
    __tablename__ = 'roles'
    
    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False, unique=True)
    
    # Relação com User: uma Role pode ter muitos Users
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"
