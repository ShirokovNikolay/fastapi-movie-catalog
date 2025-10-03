from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel, Field

NameString = Annotated[
    str,
    MaxLen(20),
]

DescriptionString = Annotated[
    str,
    MaxLen(200),
]

RatingString = Annotated[
    int,
    Field(
        ge=1,
        le=10,
    ),
]


class MovieBase(BaseModel):
    name: NameString
    description: DescriptionString = ""
    rating: RatingString


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


class MovieRead(MovieBase):
    """
    Модель для чтения данных о фильме.
    """


class MovieUpdate(MovieBase):
    """
    Модель для обновления информации о фильме.
    """


class MoviePartialUpdate(BaseModel):
    """
    Модель для частичного обновления информации о фильме.
    """

    name: NameString | None = None
    description: DescriptionString | None = None
    rating: RatingString | None = None


class Movie(MovieBase):
    """
    Модель фильма.
    """

    slug: str
    notes: DescriptionString = "service information"
