from aiopg.sa import create_engine
from fastapi import Depends

from src.app.app import app
from src.app.config import Config
from src.app.dependencies import get_config
from src.app.meta import db_var


@app.on_event("startup")
async def setup_db(config: Config = Depends(get_config)) -> None:
    """Создает пулл соединений"""
    db_var.set(await create_engine(config.db_url))


@app.on_event("shutdown")
async def teardown_db() -> None:
    """Закрывает пулл соединений"""
    db_var.get().close()
    await db_var.get().wait_closed()
