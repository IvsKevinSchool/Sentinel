"""
Notifications Event Observers

Event handlers that react to notifications-related events.
"""

from sqlalchemy.orm import Session
from db.session import SessionLocal

def on_notifications_created(payload: dict):
    """
    Handler for 'notifications.created' event.
    
    Args:
        payload: Event data containing notifications information
    """
    notifications_id = payload.get('notifications_id')
    name = payload.get('name')
    
    print(f"✓ Notifications '{name}' (ID: {notifications_id}) created successfully")
    
    # Add your custom logic here (send notifications, update cache, etc.)

def on_notifications_updated(payload: dict):
    """
    Handler for 'notifications.updated' event.
    
    Args:
        payload: Event data containing notifications information
    """
    notifications_id = payload.get('notifications_id')
    name = payload.get('name')
    
    print(f"✓ Notifications '{name}' (ID: {notifications_id}) updated successfully")
    
    # Add your custom logic here

def on_notifications_deleted(payload: dict):
    """
    Handler for 'notifications.deleted' event.
    
    Args:
        payload: Event data containing notifications information
    """
    notifications_id = payload.get('notifications_id')
    
    print(f"✓ Notifications (ID: {notifications_id}) deleted successfully")
    
    # Add your custom logic here
