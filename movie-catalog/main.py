from typing import Annotated

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)

from schemas.movie import Movie

app = FastAPI(
    title="Movie Catalog",
)
MOVIES = [
    Movie(
        movie_id=1,
        name="name 1",
        description="description 1",
        rating=5,
    ),
    Movie(
        movie_id=2,
        name="name 2",
        description="description 2",
        rating=7,
    ),
    Movie(
        movie_id=3,
        name="name 3",
        description="description 3",
        rating=8,
    ),
]


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }


@app.get(
    "/movies/",
    response_model=list[Movie],
)
def read_movies_list():
    return MOVIES


def prefetch_movie(movie_id: int) -> Movie:
    movie: Movie | None = next(
        (movie for movie in MOVIES if movie.movie_id == movie_id),
        None,
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with {movie_id=} not found",
    )


@app.get("/movies/{movie_id}/")
def read_movie_details(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
):
    return movie
