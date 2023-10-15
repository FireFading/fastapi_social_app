
# FastAPI template

template for FastAPI application with Postgres db with alembic in docker


## Features

- run app in docker
- pytest init config with main fixtures for async testing
- base CRUD for async actions with database via sqlalchemy
- alembic migrations
- github CI/CD
- formatting and linting with Nox
- main commands for actions with project in Makefile


## Installation

- use this template
- add environment variables, change .env.example to .env
- add `versions/` folder to `migrations/` folder
- add application's files to `app/` folder and pytest files to `test/` folder
## Run Locally

Alternatives for this commands you can find in Makefile

- build and run application

```bash
  docker compose up --build
```

- enter to postgres container

```bash
  docker exec -it postgres psql -U postgres
```

- enter to fastapi container

```bash
  docker exec -it fastapi bash
```

- make migrations (in fastapi docker container)

```bash
  alembic revision --autogenerate -m "<migration name>"
```

- apply migrations (in fastapi docker container)

```bash
  alembic upgrade head
```

- down docker

```bash
    docker compose down -v && docker network prune --force
```


## Running Tests

To run tests, run the following command

```bash
  pytest .
```


## Formatting & linting

- run ufmt: `ufmt format .`
- run black: `black --config=configs/.black.toml app`
- run ruff: `ruff check --config=configs/.ruff.toml --fix app`
- run flake8: `flake8 --config=configs/.flake8 app`

- OR `nox` in root

