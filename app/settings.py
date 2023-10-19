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


class MailSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env.example", env_file_encoding="utf-8", extra="allow")

    domain_name: str
    mail_username: str
    mail_password: str
    mail_port: int
    mail_server: str
    mail_starttls: bool
    mail_ssl_tls: bool
    mail_from: str
    mail_from_name: str
    mail_validate_certs: bool


class OAuth2Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env.example", env_file_encoding="utf-8", extra="allow")

    google_client_id: str
    google_client_secret: str

    github_client_id: str
    github_client_secret: str
