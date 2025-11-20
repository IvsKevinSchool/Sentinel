"""
Notifications Repository

Handles database operations for notificationss.
"""

from sqlalchemy.orm import Session

from modules.core.repositories.base_repository import BaseRepository
from modules.notifications.models.notifications_model import Notifications

class NotificationsRepository(BaseRepository[Notifications]):
    """
    Repository for Notifications entity operations.
    
    Inherits all CRUD operations from BaseRepository and adds
    custom queries specific to Notifications entity.
    
    Attributes:
        model (Type[Notifications]): The Notifications model class passed to BaseRepository.
    """

    def __init__(self):
        """
        Initialize NotificationsRepository with Notifications model.
        
        Calls parent BaseRepository.__init__ with Notifications model to set up
        base CRUD operations for the Notifications entity.
        """
        super().__init__(Notifications)

    def get_by_name(self, db: Session, name: str) -> Notifications | None:
        """
        Search notifications by name.
        
        Args:
            db (Session): SQLAlchemy database session.
            name (str): Name to search for.
        
        Returns:
            Notifications | None: Notifications instance if found, None otherwise.
        """
        return db.query(self.model).filter(self.model.name == name).first()
    
    def get_active(self, db: Session):
        """
        Get all active notificationss.
        
        Args:
            db (Session): SQLAlchemy database session.
        
        Returns:
            List[Notifications]: List of active notificationss.
        """
        return db.query(self.model).filter(self.model.is_active == True).all()
