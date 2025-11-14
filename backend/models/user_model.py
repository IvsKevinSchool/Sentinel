from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from enum import Enum
from db.session import Base

class RoleEnum(str, Enum):
    """
    DEFAULT ROLES:
    - Administrator
    - Feet Manager
    - Driver
    """
    Administrator = "Administrator"
    FeetManager = "Feet Manager"
    Driver = "Driver"

# RECUERDA VOLVER ACTIVAR AUTOCOMPLETADO:
# > Copilot: Enable Autocompletations
class User(Base):
    """
    User model.
    - id:       (int)
    - name:     (string)
    - email:    (string)
    - password: (string)
    - role:     (Enum: ["Administrator", "Feet Manager", "Driver"] )
    """
    __tablename__ = 'users'

    role_choices = [
        "Administrator",
        "Feet Manager",
        "Driver"
    ]

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(SqlEnum(RoleEnum), default=RoleEnum.FeetManager)
