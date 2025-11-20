from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.session import Base, engine

from modules.core.events.event_bus import EventBus
from modules.notifications.observers.user_notification_observers import on_user_created

from modules.users.routes import api_router

# Create all tables on DB
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Register all event handlers on application startup.
    
    This function subscribes observer functions to specific events in the EventBus.
    When events are published (e.g., 'user.created'), all subscribed observers
    are automatically notified and execute their logic.
    
    Event Subscriptions:
        - user.created: Creates welcome notification for new users
        - user.updated: Notifies user about profile changes
        - user.deleted: Logs deletion and cleans up notifications
        - user.logged_in: Creates security notification for logins
        - user.password_changed: Alerts user about password changes
    
    Architecture:
        This follows the Observer/Pub-Sub pattern where:
        - Publishers: UserService methods that publish events
        - Subscribers: Observer functions in user_event_observers
        - EventBus: Mediator that routes events to subscribers
    """

    # Startup: Subscribe events
    EventBus.suscribe('user.created', on_user_created)

    yield
    # Shutdown: Clear logic
    # EventBus.clear()

app = FastAPI(docs_url="/", lifespan=lifespan)

# Include principal router with base prefix
app.include_router(api_router, prefix="/api")


