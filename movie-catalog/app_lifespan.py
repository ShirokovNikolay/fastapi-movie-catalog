from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    # Действия перед запуском приложения.
    yield
    # Действия перед завершением работы приложения.
