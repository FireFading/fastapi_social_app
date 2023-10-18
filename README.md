## Features
- JWT-authentication
- create private chat
- update user info
- upload avatar to user profile
- change user password
- add member to chat
- get all chats allowed to user
- get messages from chat
- send message to chat via websockets
- mark message as read

## Installation
- in env.example all variables used in project, change it to .env, several variables that are common, already define as example, secret variables is empty

## Run Locally
```bash
  docker compose up --build
```
OR `make build` - first time
```bash
  docker compose up
```
OR `make up` - run without building, also you can prove -d flag to run as daemon

## Down docker
```bash
  docker compose down && docker network prune --force
```
OR `make down`

## Database
- connect to postgres
```bash
  docker exec -it postgres psql -U postgres
```
OR `make postgres`

## Migrations
- run docker containers
- connect to docker container
```bash
  docker exec -it fastapi bash
```
- apply migrations in fastapi container
```bash
  alembic upgrade head
```
- create new migrations in fastapi container
```bash
  alembic revision --autogenerate -m "<migration name>"
```
## Formatting and Linting
- formatting & linting run in `github actions`
- run ufmt: `ufmt format .`
- run black: `black --config=configs/.black.toml app`
- run ruff: `ruff check --config=configs/.ruff.toml --fix app`
- run flake8: `flake8 --config=configs/.flake8 app`

- OR `nox` in root

## Run tests
- all tests run in `github actions`
```bash
  pytest .
```
OR `pytest ./tests` OR run `nox`
- run coverage
```bash
  coverage run -m pytest
```
OR in `nox`