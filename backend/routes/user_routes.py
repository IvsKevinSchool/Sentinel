from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db 
from services.user_service import UserService
from schemas.user_schema import UserCreateSchema, UserResponseSchema 

class UserRoutes:
    def __init__(self):
        self.router = APIRouter()
        self.service = UserService()

        self.router.get("/", response_model=list[UserResponseSchema])(self.get_users)
        self.router.post("/", response_model=UserResponseSchema)(self.create_user)

    def get_users(self, db: Session = Depends(get_db)):
        return self.service.get_users(db)

    def create_user(self, data: UserCreateSchema, db: Session = Depends(get_db)):
        return self.service.create_user(db, data)

# Export user routes to principal router
user_routes = UserRoutes().router
