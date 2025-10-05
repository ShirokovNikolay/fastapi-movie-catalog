from unittest import TestCase

from schemas.movie import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)


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

    def test_movie_create_accepts_different_names(self) -> None:
        names = [
            "some-name",
            "new-name",
            "some-other-name",
            "name " * 4,
        ]
        for name in names:
            with self.subTest(name=name, msg=f"test-name - {name}"):
                movie_create = MovieCreate(
                    slug="some-slug",
                    name=name,
                    description="some-description",
                    rating=7,
                )
                self.assertEqual(name, movie_create.name)

    def test_movie_create_accepts_different_descriptions(self) -> None:
        descriptions = [
            "some-description",
            "new-description",
            "some-other-description",
            "description " * 5,
        ]
        for description in descriptions:
            with self.subTest(
                description=description,
                msg=f"test-description - {description}",
            ):
                movie_create = MovieCreate(
                    slug="some-slug",
                    name="some-name",
                    description=description,
                    rating=8,
                )
                self.assertEqual(description, movie_create.description)

    def test_movie_create_accepts_different_ratings(self) -> None:
        for rating in range(1, 11):
            with self.subTest(rating=rating, msg=f"test-rating - {rating}"):
                movie_create = MovieCreate(
                    slug="some-slug",
                    name="some-name",
                    description="some-description",
                    rating=rating,
                )
                self.assertEqual(rating, movie_create.rating)


class MovieUpdateTestCase(TestCase):
    def test_movie_update_schema_correctly_updates_the_movie_schema(self) -> None:
        movie_in = MovieCreate(
            slug="some-slug",
            name="some-name",
            description="some-description",
            rating=7,
        )

        movie = Movie(**movie_in.model_dump())

        movie_update = MovieUpdate(
            name="new-name",
            description="new-description",
            rating=10,
        )

        for field, value in movie_update:
            setattr(movie, field, value)
            assert getattr(movie, field) == value


class MoviePartialUpdateTestCase(TestCase):
    def test_empty_movie_partial_update_schema_correctly_updates_the_movie_schema(
        self,
    ) -> None:
        movie_in = MovieCreate(
            slug="some-slug",
            name="some-name",
            description="some-description",
            rating=7,
        )

        movie = Movie(**movie_in.model_dump())
        movie_copy = movie.model_copy()
        movie_empty_partial_update = MoviePartialUpdate()

        for field, value in movie_empty_partial_update:
            if value is not None:
                setattr(movie, field, value)
                assert getattr(movie, field) == value
            else:
                assert getattr(movie, field) == getattr(movie_copy, field)

    def test_movie_partial_update_schema_correctly_updates_the_movie_schema(
        self,
    ) -> None:
        movie_in = MovieCreate(
            slug="some-slug",
            name="some-name",
            description="some-description",
            rating=7,
        )

        movie = Movie(**movie_in.model_dump())
        movie_copy = movie.model_copy()
        movie_partial_update = MoviePartialUpdate(
            name="new-name",
            description="new-description",
        )

        for field, value in movie_partial_update:
            if value is not None:
                setattr(movie, field, value)
                assert getattr(movie, field) == value
            else:
                assert getattr(movie, field) == getattr(movie_copy, field)
