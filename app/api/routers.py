"""This module includes API routers."""
from fastapi import APIRouter
from .endpoints.performance import router as perf_router
router = APIRouter()

# Routers from each endpoint
router.include_router(perf_router)
