"""
Notifications Model

Database model for notifications entity.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from db.session import Base

class Notifications(Base):
    """
    Notifications model.
    
    Attributes:
        id: Primary key
        name: Notifications name
        description: Notifications description
        is_active: Status flag
        created_at: Timestamp when notifications was created
        updated_at: Timestamp when notifications was last updated
    """
    __tablename__ = 'notificationss'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
