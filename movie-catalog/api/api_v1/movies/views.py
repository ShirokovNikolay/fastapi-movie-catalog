from typing import Annotated
from fastapi import Depends, APIRouter

from .crud import MOVIES
from .dependencies import prefetch_movie
from schemas.movie import Movie

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
def read_movies_list():
    return MOVIES


@router.get("/{movie_id}/")
def read_movie_details(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
):
    return movie
