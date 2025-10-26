from typing import reveal_type

from redis import Redis

from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def add(a: int, b: int) -> int:
    return a + b


def main() -> None:
    a = 1
    b = 2
    c = add(a, b)
    print("Type c:", type(c))
    reveal_type(c)
    print(redis.ping())
    redis.set("name", "Nikolay")
    redis.set("foo", "bar")
    redis.set("number", "42")
    print(
        [
            redis.get("foo"),
            redis.get("number"),
            redis.get("spam"),
        ],
    )
    redis.delete("name")


if __name__ == "__main__":
    main()
