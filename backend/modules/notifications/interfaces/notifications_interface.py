"""
Notification Interface Module

Defines the contract for notification services using Protocol (structural typing).
Any class implementing these methods can be used as a notification service.
"""

from typing import Protocol, List
from sqlalchemy.orm import Session

class INotificationService(Protocol):
    """
    Interface for notification services.
    
    This protocol defines the contract that any notification service must implement.
    Using Protocol allows for structural typing without explicit inheritance.
    """
    
    def get_notifications(self, db: Session) -> List:
        """Get all notifications"""
        ...
    
    def get_notification_by_id(self, db: Session, id: int):
        """Get notification by ID"""
        ...
    
    def create_notification(self, db: Session, data: dict):
        """Create a new notification"""
        ...
    
    def update_notification(self, db: Session, data: dict, id: int):
        """Update an existing notification"""
        ...
    
    def delete_notification(self, db: Session, id: int):
        """Delete a notification"""
        ...

    def send_welcome_email(self, email: str):
        """Welcome message for new user"""
        ...