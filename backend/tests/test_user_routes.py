import pytest
from fastapi import status

class TestUserRoutes:
    """
    Integration test for user routes
    """
    
    def test_create_user(self, client):
        """
        Create new user test
        """
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password",
            "role": "Driver"
        }
        
        response = client.post("/api/users/", json=user_data)

        assert response.status_code == status.HTTP_200_OK
        
        data = response.json() # Parse response to JSON

        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert "id" in data    