"""
Notifications Tests

Unit tests for notifications endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db.session import Base, get_db

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_notifications.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_notifications():
    """Test creating a new notifications"""
    response = client.post(
        "/api/notificationss/",
        json={
            "name": "Test Notifications",
            "description": "Test description",
            "is_active": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Notifications"
    assert "id" in data

def test_get_notificationss():
    """Test getting all notificationss"""
    # Create a notifications first
    client.post(
        "/api/notificationss/",
        json={"name": "Test Notifications", "description": "Test"}
    )
    
    response = client.get("/api/notificationss/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_notifications_by_id():
    """Test getting notifications by ID"""
    # Create a notifications
    create_response = client.post(
        "/api/notificationss/",
        json={"name": "Test Notifications", "description": "Test"}
    )
    notifications_id = create_response.json()["id"]
    
    response = client.get(f"/api/notificationss/{notifications_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == notifications_id

def test_update_notifications():
    """Test updating a notifications"""
    # Create a notifications
    create_response = client.post(
        "/api/notificationss/",
        json={"name": "Test Notifications", "description": "Test"}
    )
    notifications_id = create_response.json()["id"]
    
    # Update it
    response = client.put(
        f"/api/notificationss/{notifications_id}",
        json={"name": "Updated Notifications"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Notifications"

def test_delete_notifications():
    """Test deleting a notifications"""
    # Create a notifications
    create_response = client.post(
        "/api/notificationss/",
        json={"name": "Test Notifications", "description": "Test"}
    )
    notifications_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/api/notificationss/{notifications_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/notificationss/{notifications_id}")
    assert get_response.status_code == 404
