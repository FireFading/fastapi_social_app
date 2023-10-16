from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(dotenv_path="../")


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env.example", env_file_encoding="utf-8", extra="allow")

    database_url: str

    postgres_db: str
    postgres_host: str
    postgres_user: str
    postgres_password: str


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env.example", env_file_encoding="utf-8", extra="allow")

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    refresh_secret_key: str
