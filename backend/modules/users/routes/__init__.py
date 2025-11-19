from fastapi import APIRouter
from modules.users.routes.user_routes import user_routes

# Principal router
api_router = APIRouter()

# Include all routes with prefix
api_router.include_router(user_routes, prefix="/users", tags=["Users"])