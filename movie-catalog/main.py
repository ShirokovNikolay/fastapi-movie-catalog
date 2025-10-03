import logging

from api import router as api_router
from app_lifespan import lifespan
from core import config
from fastapi import (
    FastAPI,
    Request,
)

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)

app = FastAPI(
    title="Movie Catalog",
    lifespan=lifespan,
)
app.include_router(api_router)


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
) -> None:
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }
