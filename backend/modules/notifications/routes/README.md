# Notifications Module

This module handles all notifications-related operations following the established architecture pattern.

## Structure
notifications/
├── interfaces/ # Protocol definitions (contracts)
├── models/ # SQLAlchemy models
├── schemas/ # Pydantic schemas
├── repositories/ # Data access layer
├── services/ # Business logic layer
├── routes/ # API endpoints
├── observers/ # Event handlers
├── helpers/ # Utility functions
├── validators/ # Custom validators
├── providers/ # Dependency injection
└── tests/ # Unit tests

## Usage

### Import the router in main.py:

```python
from modules.notifications.routes import api_router as notifications_router

app.include_router(notifications_router, prefix="/api")

Register event observers in main.py:
from modules.notifications.observers.notifications_observers import (
    on_notifications_created,
    on_notifications_updated,
    on_notifications_deleted
)

@app.on_event("startup")
def register_event_handlers():
    EventBus.suscribe('notifications.created', on_notifications_created)
    EventBus.suscribe('notifications.updated', on_notifications_updated)
    EventBus.suscribe('notifications.deleted', on_notifications_deleted)

API Endpoints
    GET    /api/notificationss/ - Get all notificationss
    GET    /api/notificationss/{id} - Get notifications by ID
    POST   /api/notificationss/ - Create new notifications
    PUT    /api/notificationss/{id} - Update notifications
    DELETE /api/notificationss/{id} - Delete notifications

Events
    notifications.created - Triggered when a notifications is created
    notifications.updated - Triggered when a notifications is updated
    notifications.deleted - Triggered when a notifications is deleted
