"""
Notifications Routes

API endpoints for notifications operations.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from modules.notifications.services.notifications_service import NotificationsService
from modules.notifications.schemas.notifications_schema import (
    NotificationsResponse,
    NotificationsCreateSchema,
    NotificationsUpdateSchema
)

router = APIRouter(
    prefix="/notificationss",
    tags=["Notificationss"]
)

notifications_service = NotificationsService()

@router.get("/", response_model=List[NotificationsResponse])
def get_notificationss(db: Session = Depends(get_db)):
    """
    Get all notificationss.
    
    Args:
        db: Database session (injected)
    
    Returns:
        List of notificationss
    """
    return notifications_service.get_notificationss(db)

@router.get("/{id}", response_model=NotificationsResponse)
def get_notifications_by_id(id: int, db: Session = Depends(get_db)):
    """
    Get notifications by ID.
    
    Args:
        id: Notifications ID
        db: Database session (injected)
    
    Returns:
        Notifications instance
    """
    return notifications_service.get_notifications_by_id(db, id)

@router.post("/", response_model=NotificationsResponse, status_code=status.HTTP_201_CREATED)
def create_notifications(
    notifications: NotificationsCreateSchema,
    db: Session = Depends(get_db)
):
    """
    Create a new notifications.
    
    Args:
        notifications: Notifications data
        db: Database session (injected)
    
    Returns:
        Created notifications
    """
    return notifications_service.create_notifications(db, notifications)

@router.put("/{id}", response_model=NotificationsResponse)
def update_notifications(
    id: int,
    notifications: NotificationsUpdateSchema,
    db: Session = Depends(get_db)
):
    """
    Update an existing notifications.
    
    Args:
        id: Notifications ID
        notifications: Update data
        db: Database session (injected)
    
    Returns:
        Updated notifications
    """
    return notifications_service.update_notifications(db, notifications, id)

@router.delete("/{id}")
def delete_notifications(id: int, db: Session = Depends(get_db)):
    """
    Delete a notifications.
    
    Args:
        id: Notifications ID
        db: Database session (injected)
    
    Returns:
        Success message
    """
    return notifications_service.delete_notifications(db, id)
