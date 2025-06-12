from fastapi import APIRouter
from router import cloud_apis
from router import services

api_router = APIRouter()

api_router.include_router(cloud_apis.router)
api_router.include_router(services.router)