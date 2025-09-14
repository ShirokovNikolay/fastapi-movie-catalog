from typing import Annotated

from pydantic import BaseModel, Field

from annotated_types import MaxLen


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
        Field(ge=1, le=10),
    ]


class MovieCreate(MovieBase):
    """
    Модель для создания фильма.
    """


class Movie(MovieBase):
    """
    Модель фильма.
    """

    movie_id: Annotated[
        int,
        Field(ge=1),
    ]
