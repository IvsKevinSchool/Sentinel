from typing import Protocol
from sqlalchemy.orm import Session

from modules.users.schemas.user_schema import UserCreateSchema
from modules.users.models.user_model import User

class IUser(Protocol):

    def create_user(self, db: Session, data: UserCreateSchema) -> User:
        ...