from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(
    title="TO DO LIST",
    description="Тестовое задание",
    version="0.0.1"
)
app.include_router(router)