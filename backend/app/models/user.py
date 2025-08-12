from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    total_score: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    quiz_attempts: Mapped[List["QuizAttempt"]] = relationship(back_populates="user")
    routes: Mapped[List["Route"]] = relationship(back_populates="user")