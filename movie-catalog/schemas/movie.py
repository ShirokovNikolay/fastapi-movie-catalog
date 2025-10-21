from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel, Field

TitleString = Annotated[
    str,
    MaxLen(20),
]

DESCRIPTION_MAX_LENGTH = 200

DescriptionString = Annotated[
    str,
    MaxLen(DESCRIPTION_MAX_LENGTH),
]

RatingString = Annotated[
    int,
    Field(
        ge=1,
        le=10,
    ),
]


class MovieBase(BaseModel):
    title: TitleString
    description: DescriptionString
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
    description: DescriptionString = ""


class MovieRead(MovieBase):
    """
    Модель для чтения данных о фильме.
    """

    slug: str


class MovieUpdate(MovieBase):
    """
    Модель для обновления информации о фильме.
    """


class MoviePartialUpdate(BaseModel):
    """
    Модель для частичного обновления информации о фильме.
    """

    title: TitleString | None = None
    description: DescriptionString | None = None
    rating: RatingString | None = None


class Movie(MovieBase):
    """
    Модель фильма.
    """

    slug: str
    notes: DescriptionString = "service information"
