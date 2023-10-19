from app.settings import JWTSettings, MailSettings, OAuth2Settings, PostgresSettings
from fastapi.security import OAuth2PasswordBearer

database_settings = PostgresSettings()
jwt_settings = JWTSettings()
mail_settings = MailSettings()
oauth2_settings = OAuth2Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/", scheme_name="JWT")
