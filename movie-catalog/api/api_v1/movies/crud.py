import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)

from core.config import MOVIES_STORAGE_FILEPATH

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def init_storage_from_state(self) -> None:
        try:
            data = MovieStorage.from_state()
            log.warning("Recovered data from storage file.")
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error.")
            return None
        self.slug_to_movie.update(
            data.slug_to_movie,
        )

    def save_state(self) -> None:
        MOVIES_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Saved movies to storage file.")

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIES_STORAGE_FILEPATH.exists():
            log.info("Movies storage file doesn't exist.")
            return MovieStorage()
        return cls.model_validate_json(MOVIES_STORAGE_FILEPATH.read_text())

    def save_movie(self, movie: Movie) -> None:
        redis.hset(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

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

    def create(self, create_movie: MovieCreate) -> Movie:
        movie = Movie(**create_movie.model_dump())
        self.slug_to_movie[movie.slug] = movie
        self.save_movie(movie)
        log.info(
            "Created movie %s",
            movie,
        )
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

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
