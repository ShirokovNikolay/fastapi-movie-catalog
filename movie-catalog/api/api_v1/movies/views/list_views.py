from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import save_storage_state
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[Depends(save_storage_state)],
)


@router.get(
    "/",
    response_model=list[MovieRead],
)
def read_movies_list() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create: MovieCreate) -> Movie:
    return storage.create(movie_create)
