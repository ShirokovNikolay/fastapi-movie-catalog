from os import getenv

if getenv("TESTING") != "1":
    raise OSError(  # noqa: TRY003
        "Environment is not ready for start.",  # noqa: EM101
    )
