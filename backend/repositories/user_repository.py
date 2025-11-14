from sqlalchemy.orm import Session

from repositories.base_repository import BaseRepository
from models.user_model import User

class UserRepository(BaseRepository[User]):

    # Inheritance from BaseRepository init
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> User | None:
        """Search user by email"""
        return db.query(self.model).filter(self.model.email == email).first()