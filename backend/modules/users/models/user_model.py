from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from enum import Enum

# For each table do you want add to sqlite3, use extends from Base
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

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(SqlEnum(RoleEnum), default=RoleEnum.FeetManager)
