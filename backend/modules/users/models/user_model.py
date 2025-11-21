from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import relationship
from enum import Enum

# For each table do you want add to sqlite3, use extends from Base
from db.session import Base

class RoleEnum(str, Enum):
    """
    Enumeration for user roles.

    ROLES:
    - ADMIN: Full system access and user managment
    - FEET_MANAGER: Fleet managment and oversight capabilities
    - DRIVER: Basic access for view stats
    """
    ADMIN = "Administrator"
    FEET_MANAGER = "Feet Manager"
    DRIVER = "Driver"

# RECUERDA VOLVER ACTIVAR AUTOCOMPLETADO:
# > Copilot: Enable Autocompletations
class User(Base):
    """
    User model representing system users.

    This model stores user information and maintains relationships with 
    other entities like notifications.

    Attributes:
    - id:               (int) Primary key, unique identifier
    - name:             (str) User's full name 
    - email:            (str) User's email address (unique) 
    - password:         (str) Hashed password for authentication
    - role:             (RoleEnum) User's role in the system
    - notifications:    (relationship) List of notificaitons for this user

    
    Relationships:
        - One-to-Many with Notification: One user can have multiple notifications
    
    Example:
        >>> user = User(
        ...     name="John Doe",
        ...     email="john@example.com",
        ...     password="hashed_password",
        ...     role=RoleEnum.Driver
        ... )
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(SqlEnum(RoleEnum), default=RoleEnum.FEET_MANAGER)

    # Relationship with Notification model
    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        """String representation for debugging"""
        return f"<User id={self.id}, email={self.email}, role={self.role}>"