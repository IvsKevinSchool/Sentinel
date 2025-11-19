from pydantic import BaseModel
from modules.users.models.user_model import RoleEnum

class UserCreateSchema(BaseModel):
    """
    Schema to create new user instance.
    """
    name: str
    email: str
    password: str
    role: RoleEnum = RoleEnum.FeetManager

class UserUpdateSchema(BaseModel):
    """
    Schema to update user instance.
    """
    name: str
    email: str
    password: str
    role: RoleEnum = RoleEnum.FeetManager

class UserResponseSchema(BaseModel):
    """
    Schema user response
    """
    id: int
    name: str
    email: str
    role: str

class LoginSchema(BaseModel):
    """
    Schema to login
    - email     (str)
    - password  (str)
    """
    email: str
    password: str