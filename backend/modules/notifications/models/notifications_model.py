"""
Notifications Model

Database model for notifications entity.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from enum import Enum

from db.session import Base

class NotificationType(str, Enum):
    """
    Enumeration for notification types.

    Types:
        INFO: General information message
        WARNING: Warning or alert message
        SUCCESS: Success confirmation message
        ERROR: Error notification message
    """
    INFO = "info"
    WARNING = "warninig"
    SUCESS = "success"
    ERROR = "error"

class Notification(Base):
    """
    Notification model for storing user notifications.
    
    This models represents notifications sent to users, tracking their status
    and maintaining a relationship with the User model.

    Attributes:
        - id                    (int): Primary key, unique identifier for the notification.
        - user_id               (int): Foreign key linking to the user table.
        - title                 (str): Notification title/subject
        - message               (str): Notification content/body
        - notification_type     (str): Type of notification (info, warning, success, error)
        - is_read               (bool): Flag indicating if the notification has been read
        - created_at            (datetime): Timestamp when the notification was created
        - updated_at            (datetime): Timestamp of last update

    Relationship:
        Allows to access navigate between objects as attributes
        - Many-to-One with User: Multiple notifications can belong to one user

        Usage example:
        >>> user = relationship("User", back_populates="notifications")
        >>> notification = Notification(...)
        >>> print(notification.user.name)

    Example:
        >>> nofication = Notification(
        ...     user_id=1
        ...     title="Welcome"
        ...     message="Welcome to Sentinel"
        ...     notification_type=NotificationType.SUCCESS
        ... )
    """

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(100), nullable=False)
    message = Column(String(500), nullable=False)
    notification_type = Column(SqlEnum(NotificationType), default=NotificationType.INFO)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC), nullable=False)

    # Relationship with User model (ORM)
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        """String representation for debugging"""
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.notification_type}, read={self.is_read})>"