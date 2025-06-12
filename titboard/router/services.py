from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/services")
def services():
    return {
        "services": [
            {
                "name": "SmartScale",
                "description": "See the future of your instance usage before it happens",
                "url": "/SmartScale",
                "icon": "bi bi-smartwatch",
                "enable": True
            },
            {
                "name": "Test",
                "description": "Test project",
                "url": "/SmartScale",
                "icon": "bi bi-smartwatch",
                "enable": False
            }
        ]
    }