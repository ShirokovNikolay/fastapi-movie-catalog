import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.movies.crud import storage
from main import app
from schemas.movie import Movie
from testing.conftest import create_movie


@pytest.fixture(
    params=[
        pytest.param("com-slug", id="common slug"),
        pytest.param("new-slug", id="short slug"),
        pytest.param("abc", id="min-slug"),
        pytest.param("qwerty-abc", id="max-slug"),
    ],
)
def movie(request: SubRequest) -> Movie:
    return create_movie(request.param)


def test_delete_movie(
    movie: Movie,
    auth_client: TestClient,
) -> None:
    url = app.url_path_for(
        "delete_movie",
        slug=movie.slug,
    )
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug)
