from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Enum, JSON
from typing import Any, List
from enum import Enum as PyEnum

from app import db

class BaseModel(db.Model):
    __abstract__ = True


class UserRole(PyEnum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable = False)
    password: Mapped[str] = mapped_column(String(255), nullable = False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.USER)
    
    results: Mapped[List["CalculationResult"]] = relationship(
            "CalculationResult", 
            back_populates="user",
            cascade="all, delete-orphan" # Deletes results if the user is deleted
        )

    def __repr__(self) -> str:
        return f"<User: {self.username}, Role: {self.role}>"
    
    def get_id(self): # for UserMixin to authenticate
        return str(self.id)
    

class CalculationResult(BaseModel):
    __tablename__ = 'calculation_results'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    data: Mapped[Any] = mapped_column(JSON, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="results")