from unittest import TestCase

from schemas.movie import Movie, MovieCreate


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created_from_create_movie_schema(self) -> None:
        movie_in = MovieCreate(
            slug="some-slug",
            name="some-name",
            description="some-description",
            rating=7,
        )

        movie = Movie(**movie_in.model_dump())

        self.assertEqual(
            movie_in.slug,
            movie.slug,
        )
        self.assertEqual(
            movie_in.name,
            movie.name,
        )
        self.assertEqual(
            movie_in.description,
            movie.description,
        )
        self.assertEqual(
            movie_in.rating,
            movie.rating,
        )

    def test_all_fields_from_movie_create_schema_are_contained_in_movie_schema(
        self,
    ) -> None:
        movie_schema_fields = set(Movie.model_fields.keys())
        for field in MovieCreate.model_fields:
            assert field in movie_schema_fields
