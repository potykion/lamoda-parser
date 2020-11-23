from contextvars import ContextVar

from aiopg.sa import create_engine, Engine, SAConnection
from fastapi import FastAPI, Depends, Request

from src.app.config import Config
from src.app.dependencies import get_config
from src.app.handlers import router

app = FastAPI()

app.include_router(router)

db_var: ContextVar[Engine] = ContextVar("db_var")


@app.on_event("startup")
async def setup_db(config: Config = Depends(get_config)):
    db_var.set(await create_engine(config.db_url))


@app.on_event("shutdown")
async def teardown_db():
    db_var.get().close()
    await db_var.get().wait_closed()
