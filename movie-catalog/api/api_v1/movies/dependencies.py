from fastapi import HTTPException
from starlette import status

from .crud import MOVIES
from schemas.movie import Movie


def prefetch_movie(slug: str) -> Movie:
    movie: Movie | None = next(
        (movie for movie in MOVIES if movie.slug == slug),
        None,
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r} not found",
    )
