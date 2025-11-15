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

    def test_create_user_with_administrator_role(self, client):
        """
        Test: Create user with Administrator role
        Verifies that a user can be created with Administrator role
        """
        user_data = {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "adminpass123",
            "role": "Administrator"
        }
        
        response = client.post("/api/users/", json=user_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["role"] == "Administrator"

    def test_create_user_with_feet_manager_role(self, client):
        """
        Test: Create user with Feet Manager role
        Verifies that a user can be created with Feet Manager role
        """
        user_data = {
            "name": "Fleet Manager",
            "email": "fleet@example.com",
            "password": "fleetpass123",
            "role": "Feet Manager"
        }
        
        response = client.post("/api/users/", json=user_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["role"] == "Feet Manager"

    def test_create_user_invalid_role(self, client):
        """
        Test: Create user with invalid role
        Verifies that the system rejects invalid roles
        """
        user_data = {
            "name": "Invalid User",
            "email": "invalid@example.com",
            "password": "password",
            "role": "InvalidRole"
        }
        
        response = client.post("/api/users/", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_user_missing_fields(self, client):
        """
        Test: Create user with missing required fields
        Verifies that the system validates required fields
        """
        user_data = {
            "name": "Incomplete User",
            "email": "incomplete@example.com"
            # Missing password and role
        }
        
        response = client.post("/api/users/", json=user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_get_all_users(self, client):
        """
        Test: Get all users
        Verifies that all users can be retrieved
        """
        # Create multiple users first
        users_data = [
            {
                "name": "User 1",
                "email": "user1@example.com",
                "password": "pass1",
                "role": "Driver"
            },
            {
                "name": "User 2",
                "email": "user2@example.com",
                "password": "pass2",
                "role": "Administrator"
            },
            {
                "name": "User 3",
                "email": "user3@example.com",
                "password": "pass3",
                "role": "Feet Manager"
            }
        ]
        
        for user_data in users_data:
            client.post("/api/users/", json=user_data)
        
        # Get all users
        response = client.get("/api/users/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Verify all users are present
        emails = [user["email"] for user in data]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails
        assert "user3@example.com" in emails

    def test_get_all_users_empty(self, client):
        """
        Test: Get all users when database is empty
        Verifies that an empty list is returned when no users exist
        """
        response = client.get("/api/users/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_user_by_id(self, client):
        """
        Test: Get user by ID
        Verifies that a specific user can be retrieved by ID
        """
        # Create a user first
        user_data = {
            "name": "Specific User",
            "email": "specific@example.com",
            "password": "specificpass",
            "role": "Driver"
        }
        create_response = client.post("/api/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Get user by ID
        response = client.get(f"/api/users/{user_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["role"] == user_data["role"]

    def test_get_user_by_id_not_found(self, client):
        """
        Test: Get user by non-existent ID
        Verifies that 404 is returned when user doesn't exist
        """
        response = client.get("/api/users/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data

    def test_update_user(self, client):
        """
        Test: Update existing user
        Verifies that a user's information can be updated
        """
        # Create a user first
        user_data = {
            "name": "Original Name",
            "email": "original@example.com",
            "password": "originalpass",
            "role": "Driver"
        }
        create_response = client.post("/api/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Update the user
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "password": "updatedpass",
            "role": "Administrator"
        }
        response = client.put(f"/api/users/{user_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]
        assert data["role"] == update_data["role"]
        
        # Verify the update persisted
        get_response = client.get(f"/api/users/{user_id}")
        get_data = get_response.json()
        assert get_data["name"] == update_data["name"]
        assert get_data["email"] == update_data["email"]

    def test_update_user_not_found(self, client):
        """
        Test: Update non-existent user
        Verifies that 404 is returned when trying to update non-existent user
        """
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "password": "updatedpass",
            "role": "Driver"
        }
        response = client.put("/api/users/99999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user(self, client):
        """
        Test: Delete existing user
        Verifies that a user can be deleted
        """
        # Create a user
        user_data = {
            "name": "User To Delete",
            "email": "delete@example.com",
            "password": "deletepass",
            "role": "Driver"
        }
        create_response = client.post("/api/users/", json=user_data)
        user_id = create_response.json()["id"]
        
        # Delete the user
        response = client.delete(f"/api/users/{user_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert str(user_id) in data["message"]
        
        # Verify user is deleted
        get_response = client.get(f"/api/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_user_not_found(self, client):
        """
        Test: Delete non-existent user
        Verifies that 404 is returned when trying to delete non-existent user
        """
        response = client.delete("/api/users/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_login_success(self, client):
        """
        Test: Successful login
        Verifies that a user can login with correct credentials
        """
        # Create a user
        user_data = {
            "name": "Login User",
            "email": "login@example.com",
            "password": "loginpass123",
            "role": "Driver"
        }
        client.post("/api/users/", json=user_data)
        
        # Attempt login
        login_data = {
            "email": "login@example.com",
            "password": "loginpass123"
        }
        response = client.post("/api/users/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == login_data["email"]
        assert data["name"] == user_data["name"]
        assert "password" not in data or data.get("password") != login_data["password"]

    def test_login_invalid_password(self, client):
        """
        Test: Login with invalid password
        Verifies that login fails with incorrect password
        """
        # Create a user
        user_data = {
            "name": "Password Test User",
            "email": "passtest@example.com",
            "password": "correctpass",
            "role": "Driver"
        }
        client.post("/api/users/", json=user_data)
        
        # Attempt login with wrong password
        login_data = {
            "email": "passtest@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/api/users/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "detail" in data
    
    def test_login_missing_fields(self, client):
        """
        Test: Login with missing fields
        Verifies that login requires both email and password
        """
        # Missing password
        login_data = {
            "email": "test@example.com"
        }
        response = client.post("/api/users/login", json=login_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    