from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    spot_id = Column(String(100), index=True)
    spot_name = Column(String(200))
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # List of options
    correct_answer = Column(Integer, nullable=False)  # Index of correct option
    explanation = Column(Text)
    difficulty = Column(String(20))  # 小学生, 中学生, 高校生, 大人
    points = Column(Integer, default=10)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    attempts = relationship("QuizAttempt", back_populates="quiz")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    route_id = Column(Integer, ForeignKey("routes.id"))
    selected_answer = Column(Integer)
    is_correct = Column(Boolean)
    points_earned = Column(Integer, default=0)
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    route = relationship("Route", back_populates="quiz_attempts")