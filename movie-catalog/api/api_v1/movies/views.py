import random
from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)

from .crud import MOVIES
from .dependencies import prefetch_movie
from schemas.movie import Movie, MovieBase

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_in: Annotated[MovieBase, Form()],
):
    return Movie(
        movie_id=random.randint(1, 10),
        **movie_in.model_dump(),
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
