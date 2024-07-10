from fastapi import APIRouter
from api.endpoints import parse


router = APIRouter()

router.include_router(parse.router, tags=["Parse"])