from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.user_repository import UserRepository
from schemas.user_schema import UserCreateSchema

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_users(self, db: Session):
        return self.repository.get_all(db)
    
    def get_user_by_id(self, db: Session, id: int):
        user = self.repository.get(db, id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return self.repository.get(db, id)

    def create_user(self, db: Session, data: UserCreateSchema):
        return self.repository.create(db, data.model_dump())
    
    def update_user(self, db: Session, data, id: int):
        return self.repository.update(db, data, id)
    
    def delete_user(self, db: Session, id: int):
        return self.repository.delete(db, id)