from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api.deps import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.models.quiz import Quiz, QuizAttempt
from app.schemas.quiz import QuizCreate, QuizResponse, QuizAttemptCreate, QuizAttemptResponse
from app.services.quiz import quiz_service
from app.services.openai_service import openai_service

router = APIRouter()

@router.post("/generate", response_model=Dict[str, Any])
async def generate_quiz(
    spot_data: Dict[str, Any],
    difficulty: str = "中学生",
    current_user: User = Depends(get_current_active_user)
):
    # Generate quiz using the service (fallback method)
    quiz_data = await quiz_service.generate_quiz(spot_data, difficulty)
    return quiz_data

@router.post("/generate-ai", response_model=Dict[str, Any])
async def generate_ai_quiz(
    spot_name: str,
    spot_description: str,
    difficulty: str = "中学生"
):
    """
    OpenAI APIを使用した動的クイズ生成
    認証不要でフロントエンドから直接呼び出し可能
    """
    # OpenAI APIでクイズ生成を試行
    quiz_data = await openai_service.generate_quiz(
        spot_name=spot_name,
        spot_description=spot_description, 
        difficulty=difficulty
    )
    
    # OpenAI API失敗時はフォールバック
    if not quiz_data:
        quiz_data = await quiz_service.generate_quiz({
            "name": spot_name,
            "description": spot_description
        }, difficulty)
    
    return {
        "success": True,
        "quiz": quiz_data,
        "generated_by": "openai" if quiz_data and quiz_data.get("question") else "fallback"
    }

@router.post("/save", response_model=QuizResponse)
async def save_quiz(
    quiz_data: QuizCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if quiz already exists for this spot
    result = await db.execute(
        select(Quiz).where(
            Quiz.spot_id == quiz_data.spot_id,
            Quiz.question == quiz_data.question
        )
    )
    existing_quiz = result.scalar_one_or_none()
    
    if existing_quiz:
        return existing_quiz
    
    # Create new quiz
    db_quiz = Quiz(**quiz_data.dict())
    db.add(db_quiz)
    await db.commit()
    await db.refresh(db_quiz)
    
    return db_quiz

@router.post("/attempt", response_model=QuizAttemptResponse)
async def submit_quiz_attempt(
    attempt_data: QuizAttemptCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Get the quiz
    result = await db.execute(
        select(Quiz).where(Quiz.id == attempt_data.quiz_id)
    )
    quiz = result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Check if correct
    is_correct = attempt_data.selected_answer == quiz.correct_answer
    points_earned = quiz.points if is_correct else 0
    
    # Create attempt record
    db_attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=attempt_data.quiz_id,
        route_id=attempt_data.route_id,
        selected_answer=attempt_data.selected_answer,
        is_correct=is_correct,
        points_earned=points_earned
    )
    db.add(db_attempt)
    
    # Update user's total score
    if is_correct:
        current_user.total_score += points_earned
    
    await db.commit()
    await db.refresh(db_attempt)
    
    return db_attempt

@router.get("/history", response_model=List[QuizAttemptResponse])
async def get_quiz_history(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(QuizAttempt)
        .where(QuizAttempt.user_id == current_user.id)
        .order_by(QuizAttempt.attempted_at.desc())
        .offset(skip)
        .limit(limit)
    )
    attempts = result.scalars().all()
    return attempts

@router.get("/spot/{spot_id}", response_model=List[QuizResponse])
async def get_quizzes_by_spot(
    spot_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Quiz).where(Quiz.spot_id == spot_id)
    )
    quizzes = result.scalars().all()
    return quizzes