# FastAPI Movie Catalog

[![Python Checks](https://img.shields.io/github/actions/workflow/status/ShirokovNikolay/fastapi-url-shortener/python-checks.yaml?branch=master&label=Python%20Checks&logo=github&logoColor=white&color=2088FF&style=for-the-badge)](https://github.com/ShirokovNikolay/fastapi-url-shortener/actions/workflows/python-checks.yaml)
[![Python](https://img.shields.io/badge/Python-3.13+-FFD43B?logo=python&logoColor=3776AB&style=for-the-badge)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-framework-009688?logo=fastapi&logoColor=white&style=for-the-badge)](https://fastapi.tiangolo.com)
[![Black](https://img.shields.io/badge/Black-formatter-000000?logo=python&logoColor=white&style=for-the-badge)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/Ruff-linter-FCC21B?logo=ruff&logoColor=black&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/Mypy-checked-1F5082?logo=python&logoColor=white&style=for-the-badge)](http://mypy-lang.org/)
[![uv](https://img.shields.io/badge/uv-managed-00C853?logo=uv&logoColor=white&style=for-the-badge)](https://github.com/astral-sh/uv)
[![Pre-commit](https://img.shields.io/badge/Pre--commit-enabled-00C853?logo=precommit&logoColor=white&style=for-the-badge)](https://pre-commit.com)

## Develop

Check GitHub Actions after any push.


### Setup:

Right click `movie-catalog` -> Mark Directory as -> Sources Root


### Install dependencies

Install all packages:
```shell
uv install
```

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Run

Go to workdir:
```shell
cd movie-catalog
```

Run dev server:
```shell
fastapi dev
```

## Snippets

```shell
python -c 'import secrets;print(secrets.token_urlsafe(16))'
```
