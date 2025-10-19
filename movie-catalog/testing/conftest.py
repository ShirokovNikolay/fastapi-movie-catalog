import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.movies.crud import storage
from schemas.movie import Movie, MovieCreate

if getenv("TESTING") != "1":
    pytest.exit(
        "Environment is not ready for start.",
    )


def build_movie_create(
    slug: str,
    description: str = "some-description",
) -> MovieCreate:
    return MovieCreate(
        slug=slug,
        name="some-movie-name",
        description=description,
        rating=8,
    )


def build_movie_create_random_slug(
    description: str = "some-description",
) -> MovieCreate:
    return MovieCreate(
        slug="".join(
            random.choices(  # noqa: S311
                string.ascii_letters,
                k=8,
            ),
        ),
        name="some-movie-name",
        description=description,
        rating=8,
    )


def create_movie(
    slug: str,
    description: str = "some-description",
) -> Movie:
    movie_in = build_movie_create(
        slug=slug,
        description=description,
    )
    return storage.create(movie_in)


def create_movie_random_slug(
    description: str = "some-description",
) -> Movie:
    movie_in = build_movie_create_random_slug(
        description=description,
    )
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)
