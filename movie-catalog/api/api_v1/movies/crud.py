from schemas.movie import Movie, MovieCreate


class MovieStorage:
    slug_to_movie: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, create_movie: MovieCreate) -> Movie:
        movie = Movie(**create_movie.model_dump())
        self.slug_to_movie[movie.slug] = movie
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(movie.slug)


storage = MovieStorage()
storage.create(
    MovieCreate(
        slug="search",
        name="name 1",
        description="description 1",
        rating=5,
    ),
)

storage.create(
    MovieCreate(
        slug="leetcode",
        name="name 2",
        description="description 2",
        rating=7,
    ),
)
