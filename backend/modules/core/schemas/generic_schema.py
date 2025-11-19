from pydantic import BaseModel

class MessageResponse(BaseModel):
    """Generic schema to message response"""
    message: str