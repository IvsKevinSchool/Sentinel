from sqlalchemy.orm import Session
from db.session import SessionLocal

from modules.notifications.services.notifications_service import NotificationService

# Initialize service
notification_service = NotificationService()

def on_user_created(payload: dict):
    """
    Handler for 'user.created' event.
    
    Creates a welcome notification when a new user is registered in the system.
    This handler is automatically triggered when the User service publishes
    a 'user.created' event.
    
    Args:
        payload: Event data containing:
            - user_id (int): ID of the newly created user
            - username (str): Name of the user
            - email (str): Email of the user
            - role (str): User's role in the system
    
    Side Effects:
        - Creates a welcome notification in the database
        - Logs the action to console
    
    Example Event Payload:
        {
            'user_id': 1,
            'username': 'John Doe',
            'email': 'john@example.com',
            'role': 'Driver'
        }
    """
    db: Session = SessionLocal()
    try:
        fk_user = payload.get('fk_user')
        username = payload.get('username')
        
        # Create welcome notification
        notification_service.create_notification(
            db,
            fk_user=fk_user,
            title="¡Bienvenido a Sentinel!",
            message=f"Hola {username}, tu cuenta ha sido creada exitosamente. "
                   f"Estamos felices de tenerte en nuestro sistema de gestión de flotas.",
            notification_type="success"
        )
        
        print(f"✓ Welcome notification sent to user {username} (ID: {fk_user})")
        
    except Exception as e:
        print(f"✗ Error creating welcome notification: {e}")
        db.rollback()
    finally:
        db.close()