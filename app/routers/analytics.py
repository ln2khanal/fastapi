from app.lib.utils import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/analytics")


@router.get(
    "/run",
    description="Runs the analytics and returns the results.",
)
async def run_analytics_not_functional(db: Session = Depends(get_db)):
    return {}
