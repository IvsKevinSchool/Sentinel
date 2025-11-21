"""
Notifications Schemas

Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class NotificationBase(BaseModel):
    """
    Base notification schema with common attributes.

    This schema contains the core fields that are shared across
    different notification operations.
    """
    title: str = Field(..., min_length=1, max_length=100, description="Notification title")
    message: str = Field(..., min_length=1, max_length=500, description="Notification message content")
    notification_type: str = Field(default="info", description="Types: info, warning, success, error")


class NotificationCreateSchema(NotificationBase):
    """
    Schema for creating a new notification

    Used when manually creating notifications or when the system
    needs to create notifications for specific users.
    
    Attributes:
        user_id: ID of the user who will receive the notification
        title: Notification title
        message: Notification content
        notification_type: Type of notification
    """
    user_id: int = Field(..., gt=0, description="ID of the user to notify")

class NotificationUpdateSchema(BaseModel):
    """
    Schema for updating notification properties.
    
    Currently only supports marking notifications as read.
    All fields are optional to allow partial updates.
    """
    is_read: Optional[bool] = Field(None, description="Mark notification as read/unread")

class NotificationResponse(NotificationBase):
    """
    Schema for notification responses.
    
    This schema is used when returning notification data to clients.
    Includes all fields from the database model.
    
    Attributes:
        id:                 Notification unique identifier
        user_id:            ID of the user who owns the notification
        is_read:            Whether the notification has been read
        created_at:         When the notification was created
        updated_at:         When the notification was last modified
    """
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class NotificationSummary(BaseModel):
    """
    Summary schema for notification statistics.
    
    Used to return aggregated information about user notifications.
    """
    total: int = Field(description="Total number of notifications")
    unread: int = Field(description="Number of unread notifications")
    
    model_config = ConfigDict(from_attributes=True)