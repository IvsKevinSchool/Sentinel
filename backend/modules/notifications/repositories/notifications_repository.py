"""
Notifications Repository

Handles database operations for notificationss.
"""

from sqlalchemy.orm import Session
from typing import List, Optional

from modules.core.repositories.base_repository import BaseRepository
from modules.notifications.models.notifications_model import Notification

class NotificationRepository(BaseRepository[Notification]):
    """
    Repository for Notifications entity operations.
    
    Inherits all CRUD operations from BaseRepository and adds
    custom queries specific to Notifications entity.
    
    Attributes:
        model (Type[Notification]): The Notifications model class passed to BaseRepository.
    """

    def __init__(self):
        """
        Initialize NotificationsRepository with Notifications model.
        
        Calls parent BaseRepository.__init__ with Notifications model to set up
        base CRUD operations for the Notifications entity.
        """
        super().__init__(Notification)


    def get_by_user_id(self, db: Session, user_id: int):
        """
        Retrieve all notifications for a specific user.
        
        Returns notifications ordered by creation date (newest first).
        
        Args:
            db: SQLAlchemy database session
            user_id: ID of the user whose notifications to retrieve
        
        Returns:
            List of Notification objects ordered by created_at DESC
        
        Example:
            >>> repo = NotificationRepository()
            >>> notifications = repo.get_by_user_id(db, user_id=1)
            >>> print(f"User has {len(notifications)} notifications")
        """
        return db.query(self.model).filter(self.model.fk_user==user_id)\
        .order_by(self.model.created_at.desc()).all()
    
    def get_unread_by_user_id(self, db: Session, user_id: int) -> List[Notification]:
        """
        Retrieve all unread notifications for a specific user.
        
        Args:
            db: SQLAlchemy database session
            user_id: ID of the user
        
        Returns:
            List of unread Notification objects ordered by created_at DESC
        
        Example:
            >>> repo = NotificationRepository()
            >>> unread = repo.get_unread_by_user_id(db, user_id=1)
            >>> print(f"User has {len(unread)} unread notifications")
        """
        return db.query(self.model)\
            .filter(
                self.model.fk_user == user_id,
                self.model.is_read == False
            )\
            .order_by(self.model.created_at.desc())\
            .all()
    
    def count_unread_by_user_id(self, db: Session, user_id: int) -> int:
        """
        Count unread notifications for a specific user.
        
        More efficient than loading all unread notifications when
        you only need the count.
        
        Args:
            db: SQLAlchemy database session
            user_id: ID of the user
        
        Returns:
            Number of unread notifications
        
        Example:
            >>> repo = NotificationRepository()
            >>> count = repo.count_unread_by_user_id(db, user_id=1)
            >>> print(f"User has {count} unread notifications")
        """
        return db.query(self.model)\
            .filter(
                self.model.fk_user == user_id,
                self.model.is_read == False
            )\
            .count()
    
    def mark_as_read(self, db: Session, notification_id: int) -> Optional[Notification]:
        """
        Mark a single notification as read.
        
        Args:
            db: SQLAlchemy database session
            notification_id: ID of the notification to mark as read
        
        Returns:
            Updated Notification object or None if not found
        
        Example:
            >>> repo = NotificationRepository()
            >>> notification = repo.mark_as_read(db, notification_id=5)
            >>> if notification:
            ...     print(f"Notification {notification.id} marked as read")
        """
        notification = self.get(db, notification_id)
        if notification:
            return self.update(db, {"is_read": True}, notification_id)
        return None
    
    def mark_all_as_read_by_user(self, db: Session, user_id: int) -> int:
        """
        Mark all unread notifications as read for a user.
        
        Performs a bulk update for efficiency instead of updating
        one notification at a time.
        
        Args:
            db: SQLAlchemy database session
            user_id: ID of the user
        
        Returns:
            Number of notifications that were marked as read
        
        Example:
            >>> repo = NotificationRepository()
            >>> count = repo.mark_all_as_read_by_user(db, user_id=1)
            >>> print(f"{count} notifications marked as read")
        """
        count = db.query(self.model)\
            .filter(
                self.model.fk_user == user_id,
                self.model.is_read == False
            )\
            .update({"is_read": True})
        db.commit()
        return count
    
    def delete_by_user_id(self, db: Session, user_id: int) -> int:
        """
        Delete all notifications for a specific user.
        
        Used when a user is deleted or when clearing all notifications.
        
        Args:
            db: SQLAlchemy database session
            user_id: ID of the user
        
        Returns:
            Number of notifications deleted
        
        Example:
            >>> repo = NotificationRepository()
            >>> count = repo.delete_by_user_id(db, user_id=1)
            >>> print(f"{count} notifications deleted")
        """
        count = db.query(self.model)\
            .filter(self.model.fk_user == user_id)\
            .delete()
        db.commit()
        return count