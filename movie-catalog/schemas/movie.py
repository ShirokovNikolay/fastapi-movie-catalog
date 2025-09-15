from typing import Annotated

from pydantic import BaseModel, Field

from annotated_types import MaxLen, Len


class MovieBase(BaseModel):
    name: Annotated[
        str,
        MaxLen(20),
    ]
    description: Annotated[
        str,
        MaxLen(200),
    ]
    rating: Annotated[
        int,
        Field(
            ge=1,
            le=10,
        ),
    ]


class MovieCreate(MovieBase):
    """
    Модель для создания фильма.
    """

    # noinspection PyTypeHints
    slug: Annotated[
        str,
        Len(
            min_length=3,
            max_length=10,
        ),
    ]


class MovieUpdate(MovieBase):
    """
    Модель для обновления информации о фильме.
    """


class Movie(MovieBase):
    """
    Модель фильма.
    """

    slug: str
