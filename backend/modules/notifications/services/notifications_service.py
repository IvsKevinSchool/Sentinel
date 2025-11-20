"""
Notifications Service

Business logic for notifications operations.
Implements INotificationsService interface.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from modules.notifications.repositories.notifications_repository import NotificationsRepository
from modules.notifications.schemas.notifications_schema import (
    NotificationsCreateSchema, 
    NotificationsUpdateSchema
)
from modules.core.events.event_bus import EventBus

class NotificationsService:
    """
    Service layer for notifications operations.
    
    Handles business logic and coordinates between repository and controllers.
    """
    
    def __init__(self):
        """Initialize with notifications repository"""
        self.repository = NotificationsRepository()

    def get_notificationss(self, db: Session):
        """
        Get all notificationss.
        
        Args:
            db (Session): Database session
        
        Returns:
            List of notificationss
        """
        return self.repository.get_all(db)
    
    def get_notifications_by_id(self, db: Session, id: int):
        """
        Get notifications by ID.
        
        Args:
            db (Session): Database session
            id (int): Notifications ID
        
        Returns:
            Notifications instance
        
        Raises:
            HTTPException: If notifications not found
        """
        self._validate_notifications_exists(db, id)
        return self.repository.get(db, id)

    def create_notifications(self, db: Session, data: NotificationsCreateSchema):
        """
        Create a new notifications.
        
        Args:
            db (Session): Database session
            data (NotificationsCreateSchema): Notifications data
        
        Returns:
            Created notifications
        """
        notifications = self.repository.create(db, data.model_dump())
        
        # Publish event
        EventBus.publish('notifications.created', {
            'notifications_id': notifications.id,
            'name': notifications.name
        })
        
        return notifications
    
    def update_notifications(self, db: Session, data: NotificationsUpdateSchema, id: int):
        """
        Update an existing notifications.
        
        Args:
            db (Session): Database session
            data (NotificationsUpdateSchema): Update data
            id (int): Notifications ID
        
        Returns:
            Updated notifications
        """
        self._validate_notifications_exists(db, id)
        notifications = self.repository.update(db, data.model_dump(exclude_unset=True), id)
        
        # Publish event
        EventBus.publish('notifications.updated', {
            'notifications_id': notifications.id,
            'name': notifications.name
        })
        
        return notifications
    
    def delete_notifications(self, db: Session, id: int):
        """
        Delete a notifications.
        
        Args:
            db (Session): Database session
            id (int): Notifications ID
        
        Returns:
            Success message
        """
        self._validate_notifications_exists(db, id)
        
        # Publish event before deletion
        EventBus.publish('notifications.deleted', {
            'notifications_id': id
        })
        
        self.repository.delete(db, id)
        return {"message": f"Notifications with id {id} deleted successfully"}
    
    def _validate_notifications_exists(self, db: Session, id: int):
        """
        Private method to validate if the notifications instance exists.
        
        Args:
            db (Session): Database session
            id (int): Notifications ID
        
        Raises:
            HTTPException: If notifications not found
        """
        notifications = self.repository.get(db, id)
        if not notifications:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Notifications not found"
            )
        return notifications
