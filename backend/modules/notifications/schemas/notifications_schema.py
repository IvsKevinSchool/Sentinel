"""
Notifications Schemas

Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class NotificationsBase(BaseModel):
    """Base notifications schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: bool = Field(default=True)

class NotificationsCreateSchema(NotificationsBase):
    """Schema for creating a notifications"""
    pass

class NotificationsUpdateSchema(BaseModel):
    """Schema for updating a notifications"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class NotificationsResponse(NotificationsBase):
    """Schema for notifications response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
