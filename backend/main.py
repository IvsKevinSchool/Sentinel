from fastapi import FastAPI
from db.session import Base, engine

from routes import api_router

# Create all tables on DB
Base.metadata.create_all(bind=engine)


# Create FastAPI instance
app = FastAPI()

# Include principal router with base prefix
app.include_router(api_router, prefix="/api")






# Define a root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {"Hello": "World"}


