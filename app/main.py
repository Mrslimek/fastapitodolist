from fastapi import FastAPI
from app.api.routes import router
from fastapi_pagination import add_pagination


app = FastAPI(
    title="TO DO LIST",
    description="Тестовое задание",
    version="0.0.1"
)
app.include_router(router)
add_pagination(app)
