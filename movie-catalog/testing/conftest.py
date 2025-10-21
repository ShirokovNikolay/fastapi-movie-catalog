import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.movies.crud import storage
from schemas.movie import Movie, MovieCreate


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        pytest.exit(
            "Environment is not ready for start.",
        )


def build_movie_create(
    slug: str,
    title: str = "some-title",
    description: str = "some-description",
    rating: int = 8,
) -> MovieCreate:
    return MovieCreate(
        slug=slug,
        title=title,
        description=description,
        rating=rating,
    )


def build_movie_create_random_slug(
    title: str = "some-title",
    description: str = "some-description",
    rating: int = 8,
) -> MovieCreate:
    return MovieCreate(
        slug="".join(
            random.choices(  # noqa: S311
                string.ascii_letters,
                k=8,
            ),
        ),
        title=title,
        description=description,
        rating=rating,
    )


def create_movie(
    slug: str,
    title: str = "some-title",
    description: str = "some-description",
    rating: int = 8,
) -> Movie:
    movie_in = build_movie_create(
        slug=slug,
        title=title,
        description=description,
        rating=rating,
    )
    return storage.create(movie_in)


def create_movie_random_slug(
    title: str = "some-title",
    description: str = "some-description",
    rating: int = 8,
) -> Movie:
    movie_in = build_movie_create_random_slug(
        title=title,
        description=description,
        rating=rating,
    )
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)
