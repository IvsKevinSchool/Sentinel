from fastapi import FastAPI
from db.session import Base, engine

from modules.users.routes import api_router

# Create all tables on DB
Base.metadata.create_all(bind=engine)


# Create FastAPI instance
app = FastAPI(
    docs_url="/"
)

# Include principal router with base prefix
app.include_router(api_router, prefix="/api")


