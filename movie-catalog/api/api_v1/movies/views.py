from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)
from .crud import MOVIES
from .dependencies import prefetch_movie
from schemas.movie import Movie, MovieCreate

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


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create: MovieCreate):
    return Movie(
        **movie_create.model_dump(),
    )


@router.get("/{slug}/")
def read_movie_details(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
):
    return movie
