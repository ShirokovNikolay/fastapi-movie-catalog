from unittest import TestCase

from pydantic import ValidationError

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
            title="some-title",
            description="some-description",
            rating=7,
        )

        movie = Movie(**movie_in.model_dump())

        self.assertEqual(
            movie_in.slug,
            movie.slug,
        )
        self.assertEqual(
            movie_in.title,
            movie.title,
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

    def test_movie_create_accepts_different_titles(self) -> None:
        titles = [
            "some-title",
            "new-title",
            "some-other-title",
            "title " * 3,
        ]
        for title in titles:
            with self.subTest(title=title, msg=f"test-title - {title}"):
                movie_create = MovieCreate(
                    slug="some-slug",
                    title=title,
                    description="some-description",
                    rating=7,
                )
                self.assertEqual(title, movie_create.title)

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
                    title="some-title",
                    description=description,
                    rating=8,
                )
                self.assertEqual(description, movie_create.description)

    def test_movie_create_accepts_different_ratings(self) -> None:
        for rating in range(1, 11):
            with self.subTest(rating=rating, msg=f"test-rating - {rating}"):
                movie_create = MovieCreate(
                    slug="some-slug",
                    title="some-title",
                    description="some-description",
                    rating=rating,
                )
                self.assertEqual(rating, movie_create.rating)

    def test_movie_slug_too_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            MovieCreate(
                slug="s",
                title="some-title",
                description="some-description",
                rating=8,
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_short"
        self.assertEqual(
            expected_type,
            error_details["type"],
        )

    def test_movie_slug_too_short_with_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 3 characters",
        ):
            MovieCreate(
                slug="s",
                title="some-title",
                description="some-description",
                rating=8,
            )


class MovieUpdateTestCase(TestCase):
    def test_movie_update_schema_correctly_updates_the_movie_schema(self) -> None:
        movie_in = MovieCreate(
            slug="some-slug",
            title="some-title",
            description="some-description",
            rating=7,
        )

        movie = Movie(**movie_in.model_dump())

        movie_update = MovieUpdate(
            title="new-title",
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
            title="some-title",
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
            title="some-title",
            description="some-description",
            rating=7,
        )

        movie = Movie(**movie_in.model_dump())
        movie_copy = movie.model_copy()
        movie_partial_update = MoviePartialUpdate(
            title="new-title",
            description="new-description",
        )

        for field, value in movie_partial_update:
            if value is not None:
                setattr(movie, field, value)
                assert getattr(movie, field) == value
            else:
                assert getattr(movie, field) == getattr(movie_copy, field)
