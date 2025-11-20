"""
Notifications Interface Module

Defines the contract for notifications services using Protocol (structural typing).
Any class implementing these methods can be used as a notifications service.
"""

from typing import Protocol, List
from sqlalchemy.orm import Session

class INotificationsService(Protocol):
    """
    Interface for notifications services.
    
    This protocol defines the contract that any notifications service must implement.
    Using Protocol allows for structural typing without explicit inheritance.
    """
    
    def get_notificationss(self, db: Session) -> List:
        """Get all notificationss"""
        ...
    
    def get_notifications_by_id(self, db: Session, id: int):
        """Get notifications by ID"""
        ...
    
    def create_notifications(self, db: Session, data: dict):
        """Create a new notifications"""
        ...
    
    def update_notifications(self, db: Session, data: dict, id: int):
        """Update an existing notifications"""
        ...
    
    def delete_notifications(self, db: Session, id: int):
        """Delete a notifications"""
        ...
