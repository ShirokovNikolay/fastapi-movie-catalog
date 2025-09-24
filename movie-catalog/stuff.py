from redis import Redis

from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def main():
    print(redis.ping())
    redis.set("name", "Nikolay")
    redis.set("number", "42")
    redis.set("test", "True")
    print(
        [
            redis.get("name"),
            redis.get("number"),
            redis.get("spam"),
        ]
    )
    redis.delete("test")
    print(redis.get("test"))


if __name__ == "__main__":
    main()
