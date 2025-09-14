from typing import Annotated

from pydantic import BaseModel, Field

from annotated_types import MaxLen


class MovieBase(BaseModel):
    movie_id: Annotated[
        int,
        Field(ge=1),
    ]
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


class Movie(MovieBase):
    """
    Модель фильма.
    """
