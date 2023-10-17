from app.settings import JWTSettings, PostgresSettings
from fastapi.security import OAuth2PasswordBearer

database_settings = PostgresSettings()
jwt_settings = JWTSettings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/", scheme_name="JWT")
