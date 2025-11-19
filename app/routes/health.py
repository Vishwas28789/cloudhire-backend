from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "cloudhire-nexus-backend"
    }
