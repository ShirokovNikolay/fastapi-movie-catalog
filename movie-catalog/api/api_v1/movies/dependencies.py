from fastapi import HTTPException, BackgroundTasks
from starlette import status

from .crud import storage
from schemas.movie import Movie


def prefetch_movie(slug: str) -> Movie:
    movie = storage.get_by_slug(slug=slug)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r} not found",
    )

def save_storage_state(background_tasks: BackgroundTasks) -> None:
    pass