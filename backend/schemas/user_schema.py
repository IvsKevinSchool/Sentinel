from pydantic import BaseModel
from models.user_model import RoleEnum

class UserCreateSchema(BaseModel):
    """
    Schema to create new user instance.
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