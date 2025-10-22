import pytest
from starlette import status
from starlette.testclient import TestClient

from main import app


@pytest.mark.xfail(
    reason="not implemented yet",
    raises=NotImplementedError,
    strict=False,
)
def test_transfer_movie(
    auth_client: TestClient,
) -> None:
    url = app.url_path_for(
        "transfer_movie",
        slug="some-slug",
    )
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_200_OK, response.text
