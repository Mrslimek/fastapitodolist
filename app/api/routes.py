from fastapi import APIRouter
from app.api.v1.tasks import router as tasks_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router


router = APIRouter()
router.include_router(tasks_router, tags=["Tasks"])
router.include_router(users_router, tags=["Users"])
router.include_router(auth_router, tags=["Auth"])
