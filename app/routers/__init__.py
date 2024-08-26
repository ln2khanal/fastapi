from .crud import router as crud_router
from .datasource import router as sourcedata_router
from .analytics import router as analytics_router

__all__ = ["sourcedata_router", "analytics_router", "crud_router"]