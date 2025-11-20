"""
Notifications Routes Package

Exports the main API router for notifications endpoints.
"""

from fastapi import APIRouter
from .notifications_routes import router

api_router = APIRouter()
api_router.include_router(router)

__all__ = ['api_router']
