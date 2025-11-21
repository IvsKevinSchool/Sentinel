"""
Notifications Service

Business logic for notifications operations.
Implements INotificationsService interface.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Dict

from modules.notifications.repositories.notifications_repository import NotificationRepository
from modules.notifications.schemas.notifications_schema import (
    NotificationCreateSchema,
    NotificationUpdateSchema,
    NotificationResponse,
    NotificationSummary
)
from modules.notifications.models.notifications_model import Notification
from modules.core.events.event_bus import EventBus

class NotificationService:
    """
    Service layer for notification management.
    
    This service handles all business logic related to notifications,
    including creation, retrieval, updates, and deletion. It acts as
    an intermediary between the API layer and the data access layer.
    
    The service publishes events through EventBus to maintain loose
    coupling with other system components.
    
    Attributes:
        repository: NotificationRepository instance for data access
    """
    
    def __init__(self):
        """
        Initialize NotificationService with repository dependency.
        
        The repository is instantiated here, but in a more advanced
        implementation, it could be injected through the Container.
        """
        self.repository = NotificationRepository()

    def get_notifications(self, db: Session) -> List[Notification]:
        """
        Retrieve all notifications in the system.
        
        Args:
            db: Database session
        
        Returns:
            List of all Notification objects
        
        Example:
            >>> service = NotificationService()
            >>> notifications = service.get_notifications(db)
        """
        return self.repository.get_all(db)
    
    def get_user_notifications(self, db: Session, user_id: int) -> List[Notification]:
        """
        Retrieve all notifications for a specific user.
        
        Args:
            db: Database session
            user_id: ID of the user
        
        Returns:
            List of user's notifications ordered by creation date
        
        Example:
            >>> service = NotificationService()
            >>> notifications = service.get_user_notifications(db, user_id=1)
        """
        return self.repository.get_by_user_id(db, user_id)
    
    def get_unread_notifications(self, db: Session, user_id: int) -> List[Notification]:
        """
        Retrieve unread notifications for a specific user.
        
        Args:
            db: Database session
            user_id: ID of the user
        
        Returns:
            List of unread notifications
        
        Example:
            >>> service = NotificationService()
            >>> unread = service.get_unread_notifications(db, user_id=1)
        """
        return self.repository.get_unread_by_user_id(db, user_id)
    
    def get_notification_summary(self, db: Session, user_id: int) -> NotificationSummary:
        """
        Get notification statistics for a user.
        
        Provides a summary of total and unread notifications without
        loading all notification objects.
        
        Args:
            db: Database session
            user_id: ID of the user
        
        Returns:
            NotificationSummary with total and unread counts
        
        Example:
            >>> service = NotificationService()
            >>> summary = service.get_notification_summary(db, user_id=1)
            >>> print(f"Unread: {summary.unread}/{summary.total}")
        """
        all_notifications = self.repository.get_by_user_id(db, user_id)
        unread_count = self.repository.count_unread_by_user_id(db, user_id)
        
        return NotificationSummary(
            total=len(all_notifications),
            unread=unread_count
        )
    
    def get_notification_by_id(self, db: Session, notification_id: int) -> Notification:
        """
        Retrieve a specific notification by ID.
        
        Args:
            db: Database session
            notification_id: ID of the notification
        
        Returns:
            Notification object
        
        Raises:
            HTTPException: If notification not found (404)
        
        Example:
            >>> service = NotificationService()
            >>> notification = service.get_notification_by_id(db, 5)
        """
        notification = self.repository.get(db, notification_id)
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        return notification

    def create_notification(
        self, 
        db: Session, 
        user_id: int, 
        title: str, 
        message: str, 
        notification_type: str = "info"
    ) -> Notification:
        """
        Create a new notification for a user.
        
        This method creates a notification and publishes a 'notification.created'
        event that other parts of the system can react to (e.g., sending emails,
        push notifications, etc.).
        
        Args:
            db: Database session
            user_id: ID of the user to notify
            title: Notification title
            message: Notification content
            notification_type: Type of notification (info, warning, success, error)
        
        Returns:
            Created Notification object
        
        Raises:
            HTTPException: If user doesn't exist (validated by foreign key)
        
        Example:
            >>> service = NotificationService()
            >>> notification = service.create_notification(
            ...     db,
            ...     user_id=1,
            ...     title="Welcome",
            ...     message="Welcome to Sentinel!",
            ...     notification_type="success"
            ... )
        """
        notification_data = {
            "user_id": user_id,
            "title": title,
            "message": message,
            "notification_type": notification_type
        }
        
        try:
            notification = self.repository.create(db, notification_data)
            
            # Publish event for other system components
            EventBus.publish('notification.created', {
                'notification_id': notification.id,
                'user_id': user_id,
                'title': title,
                'message': message,
                'notification_type': notification_type
            })
            
            return notification
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating notification: {str(e)}"
            )
        
    def mark_as_read(self, db: Session, notification_id: int) -> Notification:
        """
        Mark a notification as read.
        
        Args:
            db: Database session
            notification_id: ID of the notification
        
        Returns:
            Updated Notification object
        
        Raises:
            HTTPException: If notification not found (404)
        
        Example:
            >>> service = NotificationService()
            >>> notification = service.mark_as_read(db, notification_id=5)
        """
        notification = self.repository.mark_as_read(db, notification_id)
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        # Publish event
        EventBus.publish('notification.read', {
            'id': notification.id,
            'user_id': notification.user_id
        })
        
        return notification

    def mark_all_as_read(self, db: Session, user_id: int) -> Dict[str, int]:
        """
        Mark all unread notifications as read for a user.
        
        Args:
            db: Database session
            user_id: ID of the user
        
        Returns:
            Dictionary with count of notifications marked as read
        
        Example:
            >>> service = NotificationService()
            >>> result = service.mark_all_as_read(db, user_id=1)
            >>> print(f"{result['count']} notifications marked as read")
        """
        count = self.repository.mark_all_as_read_by_user(db, user_id)
        
        # Publish event
        EventBus.publish('notifications.all_read', {
            'user_id': user_id,
            'count': count
        })
        
        return {"count": count, "message": f"{count} notifications marked as read"}
    
    def delete_notification(self, db: Session, notification_id: int) -> Dict[str, str]:
        """
        Delete a specific notification.
        
        Args:
            db: Database session
            notification_id: ID of the notification to delete
        
        Returns:
            Success message dictionary
        
        Raises:
            HTTPException: If notification not found (404)
        
        Example:
            >>> service = NotificationService()
            >>> result = service.delete_notification(db, notification_id=5)
        """
        notification = self.repository.get(db, notification_id)
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        user_id = notification.user_id
        self.repository.delete(db, notification_id)
        
        # Publish event
        EventBus.publish('notification.deleted', {
            'id': notification_id,
            'user_id': user_id
        })
        
        return {"message": "Notification deleted successfully"}