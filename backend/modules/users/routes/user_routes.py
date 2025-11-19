from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from db.session import get_db 
from modules.users.services.user_service import UserService
from modules.core.schemas.generic_schema import MessageResponse
from modules.users.schemas.user_schema import UserCreateSchema, UserUpdateSchema, UserResponseSchema, LoginSchema

# Create alias for db depends
DbSession = Annotated[Session, Depends(get_db)]

class UserRoutes:
    def __init__(self):
        self.router = APIRouter()
        self.service = UserService()

        self.router.get("/", response_model=list[UserResponseSchema])(self.get_users)
        self.router.get("/{id}", response_model=UserResponseSchema)(self.get_user_by_id)
        self.router.post("/", response_model=UserResponseSchema)(self.create_user)
        self.router.put("/{id}", response_model=UserResponseSchema)(self.update_user)
        self.router.delete("/{id}", response_model=MessageResponse)(self.delete_user)
        self.router.post("/login", response_model=UserResponseSchema)(self.login)

    def get_users(self, db: DbSession):
        return self.service.get_users(db)
    
    def get_user_by_id(self, id: int, db: DbSession):
        return self.service.get_user_by_id(db, id)

    def create_user(self, data: UserCreateSchema, db: DbSession):
        return self.service.create_user(db, data)
    
    def update_user(self, data: UserUpdateSchema, id: int, db: DbSession):
        return self.service.update_user(db, data, id)
    
    def delete_user(self, id: int, db: DbSession):
        return self.service.delete_user(db, id)
    
    def login(self, data: LoginSchema, db: DbSession):
        return self.service.login(db, data)

# Export user routes to principal router
user_routes = UserRoutes().router
