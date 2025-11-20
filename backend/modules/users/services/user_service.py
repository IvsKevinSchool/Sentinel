from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from modules.core.events.event_bus import EventBus
from modules.users.repositories.user_repository import UserRepository
from modules.users.schemas.user_schema import UserCreateSchema, LoginSchema

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_users(self, db: Session):
        return self.repository.get_all(db)
    
    def get_user_by_id(self, db: Session, id: int):
        self._validate_user_exists(db, id)
        return self.repository.get(db, id)

    def create_user(self, db: Session, data: UserCreateSchema):
        """
        Create a new user in the system.
        
        This method creates a user and publishes a 'user.created' event
        that triggers welcome notifications and other system reactions.
        
        Args:
            db: Database session
            data: User creation data (validated by Pydantic)
        
        Returns:
            Created User object
        
        Raises:
            HTTPException: If email already exists or validation fails
        
        Event Published:
            'user.created' with payload:
                - user_id: ID of the created user
                - username: User's name
                - email: User's email
                - role: User's role
        """
        # Check if email already exists
        existing_user = self.repository.get_by_email(db, data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user = self.repository.create(db, data.model_dump())
        
        # Publish event for notifications and other side effects
        EventBus.publish('user.created', {
            'user_id': user.id,
            'username': user.name,
            'email': user.email,
            'role': user.role
        })
        
        print(f"✓ User '{user.name}' created successfully (ID: {user.id})")
        
        return user
    
    def update_user(self, db: Session, data, id: int):
        self._validate_user_exists(db, id)
        return self.repository.update(db, data.model_dump(), id)
    
    def delete_user(self, db: Session, id: int):
        self._validate_user_exists(db, id)
        self.repository.delete(db, id)
        return { "message": f"User with id {id} deleted successfully" }
    
    def login(self, db: Session, data: LoginSchema):
        user = self.repository.get_by_email(db, data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if user.password != data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        return user
    
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