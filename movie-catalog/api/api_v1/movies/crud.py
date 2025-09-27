import logging

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)


log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """
    Base exception for movie CRUD actions.
    """


class MovieAlreadyExistsError(MovieBaseError):
    """
    Raised on movie creation if such slug already exists.
    """


class MovieStorage(BaseModel):

    def save_movie(self, movie: Movie) -> None:
        redis.hset(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )
        log.info("Saved movie to storage.")

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(value)
            for value in redis.hvals(name=config.REDIS_MOVIES_HASH_NAME)
        ]

    def get_by_slug(self, slug) -> Movie | None:
        if data := redis.hget(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=slug,
        ):
            return Movie.model_validate_json(data)

    def exists(self, slug: str) -> bool:
        return bool(
            redis.hexists(
                name=config.REDIS_MOVIES_HASH_NAME,
                key=slug,
            )
        )

    def create(self, create_movie: MovieCreate) -> Movie:
        movie = Movie(**create_movie.model_dump())
        self.save_movie(movie)
        log.info(
            "Created movie %s",
            movie,
        )
        return movie

    def create_or_raise_if_exists(self, create_movie: MovieCreate) -> Movie:
        if not self.exists(create_movie.slug):
            return self.create(create_movie)
        raise MovieAlreadyExistsError(create_movie.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            config.REDIS_MOVIES_HASH_NAME,
            slug,
        )

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)
        log.info(
            "Deleted movie %s",
            movie,
        )

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_movie(movie)
        log.info(
            "Updated movie %s",
            movie,
        )
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MoviePartialUpdate,
    ) -> Movie:
        parameters = []
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
            parameters.append("%s=%r" % (field_name, value))
        self.save_movie(movie)
        log.info(
            "Updated partial movie %s",
            " ".join(parameters),
        )
        return movie


storage = MovieStorage()
