from fastapi import APIRouter, Body

router = APIRouter()

users = [
    {"id": 1, "name": "Alice", "age": 30, "nationality": "American"},
    {"id": 2, "name": "Bob", "age": 25, "nationality": "British"},
]

"""
GET /users
Retrieve a list of all users.
"""
@router.get("/users", tags=["Users"])
async def get_user():
    return users

@router.get("/users/{id}", tags=["Users"])
async def get_user_by_id(id: int):
    for user in users:
        if user["id"] == id:
            return user

    return {"error": "User not found"}

@router.get("/user/", tags=["User"])
async def get_user_query(age: str, nationality: str):
    filtered_users = [
        user for user in users
        if user["age"] == int(age) and user["nationality"].lower() == nationality.lower()
    ]
    return filtered_users

"""
POST /users
Create a new user with the provided id and name.
"""

@router.post("/users", tags=["Users"])
async def create_user(id: int = Body(...), name: str = Body(...)):
    users.append({
        "id": id,
        "name": name
    })
    return {"Hello": f"User {name} with id {id} created"}

"""
PUT /users
Update an existing user's name by their id.
"""

@router.put("/users/{id}", tags=["Users"])
async def update_user(id: int, name: str = Body(...)):
    for user in users:
        if user["id"] == id:
            user["name"] = name
            return {"Hello": f"User with id {id} updated to name {name}"}
    return {"error": "User not found"}

"""
DELETE /users
Delete a user by their id.
"""
@router.delete("/users/{id}", tags=["Users"])
async def delete_user(id: int):
    for user in users:
        if user["id"] == id:
            users.remove(user)
            return {"Hello": f"User with id {id} deleted"}
    return {"error": "User not found"}