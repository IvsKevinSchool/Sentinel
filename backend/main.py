from fastapi import FastAPI
from crud.user_crud import router as user_router

# Create FastAPI instance
app = FastAPI()

# Include user router
app.include_router(user_router, prefix="", tags=["Users"])

# Define a root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"Hello": "World"}

@app.get("/home", tags=["Root"])
async def read_home():
    return {"Hello": "Home"}

