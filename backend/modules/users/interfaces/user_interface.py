from typing import Protocol
from sqlalchemy.orm import Session

class IUsers(Protocol):

    def get_users(self, db: Session) -> None:
        ...