from fastapi import APIRouter
from router import cloud_apis

api_router = APIRouter()

api_router.include_router(cloud_apis.router)