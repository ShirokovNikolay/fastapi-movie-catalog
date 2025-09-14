import random
from typing import Annotated

from annotated_types import MaxLen
from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)
from pydantic import Field

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


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    name: Annotated[
        str,
        MaxLen(20),
        Form(),
    ],
    description: Annotated[
        str,
        MaxLen(200),
        Form(),
    ],
    rating: Annotated[
        int,
        Field(ge=1, le=10),
        Form(),
    ],
):
    return Movie(
        movie_id=random.randint(1, 10),
        name=name,
        description=description,
        rating=rating,
    )


@router.get("/{movie_id}/")
def read_movie_details(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
):
    return movie
