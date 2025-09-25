import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    Depends,
    status,
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
)

from .crud import storage
from .redis import redis_tokens

from core.config import (
    REDIS_TOKENS_SET_NAME,
    USERS_DB,
)
from schemas.movie import Movie

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)

static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from the developer portal. [Read more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic auth",
    description="Basic username + password auth",
    auto_error=False,
)


def prefetch_movie(slug: str) -> Movie:
    movie = storage.get_by_slug(slug=slug)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r} not found.",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
) -> None:
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage.")
        background_tasks.add_task(storage.save_state)


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
) -> None:
    if not redis_tokens.sismember(
        REDIS_TOKENS_SET_NAME,
        api_token.credentials,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token.",
        )


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ],
) -> None:
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )

    validate_api_token(
        api_token=api_token,
    )


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
) -> None:
    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ],
) -> None:
    if request.method not in UNSAFE_METHODS:
        return

    validate_basic_auth(
        credentials=credentials,
    )


def api_token_or_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ],
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ],
) -> None:
    if request.method not in UNSAFE_METHODS:
        return

    log.info("User auth credentials %s", credentials)
    log.info("API token auth credentials %s", api_token)

    if credentials:
        return validate_basic_auth(
            credentials=credentials,
        )

    if api_token:
        return validate_api_token(
            api_token=api_token,
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Api token or basic auth is required.",
    )
