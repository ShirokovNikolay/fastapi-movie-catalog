from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.movies.crud import storage
from main import app
from schemas.movie import Movie, MovieUpdate
from testing.conftest import create_movie_random_slug


@pytest.mark.apitest
class TestUpdate:
    @pytest.fixture
    def movie(self, request: SubRequest) -> Generator[Movie]:
        title, description, rating = request.param
        movie = create_movie_random_slug(
            title=title,
            description=description,
            rating=rating,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_title, new_description, new_rating",
        [
            pytest.param(
                ("title", "description", 8),
                "new_title",
                "new_description",
                8,
                id="base-test",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details(
        self,
        movie: Movie,
        new_title: str,
        new_description: str,
        new_rating: int,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "update_movie_details",
            slug=movie.slug,
        )

        movie_update = MovieUpdate(
            title=new_title,
            description=new_description,
            rating=new_rating,
        )

        response = auth_client.put(
            url=url,
            json=movie_update.model_dump(mode="json"),
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(slug=movie.slug)
        assert movie_db
        assert MovieUpdate(**movie_db.model_dump()) == movie_update
