from fastapi import FastAPI

from src.app.handlers import router

app = FastAPI()

app.include_router(router)
