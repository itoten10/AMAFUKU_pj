from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QuizBase(BaseModel):
    spot_id: str
    spot_name: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    difficulty: str
    points: int = 10

class QuizCreate(QuizBase):
    pass

class QuizResponse(QuizBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class QuizAttemptCreate(BaseModel):
    quiz_id: int
    route_id: Optional[int] = None
    selected_answer: int

class QuizAttemptResponse(BaseModel):
    id: int
    quiz_id: int
    selected_answer: int
    is_correct: bool
    points_earned: int
    attempted_at: datetime
    
    class Config:
        orm_mode = True