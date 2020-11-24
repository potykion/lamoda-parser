from contextvars import ContextVar

from aiopg.sa import Engine

db_var: ContextVar[Engine] = ContextVar("db_var")
