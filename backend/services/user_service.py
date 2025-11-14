from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories.user_repository import UserRepository
from schemas.user_schema import UserCreateSchema

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_users(self, db: Session):
        return self.repository.get_all(db)
    
    def get_user_by_id(self, db: Session, id: int):
        self._validate_user_exists(db, id)
        return self.repository.get(db, id)

    def create_user(self, db: Session, data: UserCreateSchema):
        return self.repository.create(db, data.model_dump())
    
    def update_user(self, db: Session, data, id: int):
        self._validate_user_exists(db, id)
        return self.repository.update(db, data.model_dump(), id)
    
    def delete_user(self, db: Session, id: int):
        self._validate_user_exists(db, id)
        self.repository.delete(db, id)
        return { "message": f"User with id {id} deleted successfully" }
    
    def _validate_user_exists(self, db: Session, id: int):
        """Private method to validate if the user instance exist"""
        user = self.repository.get(db, id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
"""
WRAPPER FUNCTION TO VALIDATE USER (ADVANCED)

from functools import wraps

def validate_user(func):
    @wraps(func)
    def wrapper(self, db: Session, id: int, *args, **kwargs):
        user = self.repository.get(db, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return func(self, db, id, *args, **kwargs)
    return wrapper

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    @validate_user
    def get_user_by_id(self, db: Session, id: int):
        return self.repository.get(db, id)

    @validate_user
    def update_user(self, db: Session, id: int, data):
        return self.repository.update(db, data.model_dump(), id)
"""