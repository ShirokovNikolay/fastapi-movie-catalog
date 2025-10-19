from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.movies.crud import storage
from main import app
from schemas.movie import DESCRIPTION_MAX_LENGTH, Movie
from testing.conftest import create_movie_random_slug


class TestUpdatePartial:
    @pytest.fixture
    def movie(self, request: SubRequest) -> Generator[Movie]:
        movie = create_movie_random_slug(
            description=request.param,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_description",
        [
            pytest.param(
                "description",
                "",
                id="description-to-empty-description",
            ),
            pytest.param(
                "",
                "not empty description",
                id="empty-description-to-description",
            ),
            pytest.param(
                "s" * DESCRIPTION_MAX_LENGTH,
                "",
                id="max-description-to-empty-description",
            ),
            pytest.param(
                "",
                "s" * DESCRIPTION_MAX_LENGTH,
                id="empty-description-to-max-description",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details_partial(
        self,
        movie: Movie,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "update_movie_details_partial",
            slug=movie.slug,
        )
        response = auth_client.patch(
            url=url,
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK
        movie_db = storage.get_by_slug(slug=movie.slug)
        assert movie_db
        assert movie_db.description == new_description
