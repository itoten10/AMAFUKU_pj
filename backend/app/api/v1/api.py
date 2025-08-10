from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, routes, quizzes

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(routes.router, prefix="/routes", tags=["routes"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])