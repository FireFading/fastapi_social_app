## Features
- Secure Authentication: Implement JWT-based authentication for user access control.
- Private Group Chat Creation: Enable users to create group private chats for conversations.
- User Profile Customization: Allow users to update and personalize their profile information.
- Avatar Upload: Empower users to upload custom avatars to enhance their profile visibility.
- Password Management: Provide a password change feature to enhance user account security.
- Password Reset Request: Allow users to request a password reset if they've forgotten their current password.
- Chat Membership Control: Enable chat members to add/remove members to/from existing chat groups.
- User Search: Allow users to search for other users based on their usernames.
- Chat Listing: Provide users with the ability to view a list of all chat rooms they are part of.
- Message Retrieval: Allow users to access chat messages, view chat history, and scroll through past conversations.
- Real-time Messaging: Implement WebSocket support to facilitate instant message delivery in chat rooms.
- Message Status Tracking: Enable users to mark messages as read to track their interaction with chat content.

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