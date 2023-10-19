import stackprinter
import uvicorn
from app.routers.chats import router as chats_router
from app.routers.users import router as users_router
from fastapi import FastAPI
from fastapi_pagination import add_pagination

stackprinter.set_excepthook()

app = FastAPI()

add_pagination(app)
app.include_router(users_router)
app.include_router(chats_router)
# app.include_router(oauth2_router)

# app.add_middleware(
#     OAuth2Middleware,
#     config=OAuth2Config(
#         allow_http=True,
#         jwt_secret=jwt_settings.secret_key,
#         jwt_expires=jwt_settings.access_token_expire_minutes,
#         jwt_algorithm=jwt_settings.algorithm,
#         clients=[
#             OAuth2Client(
#                 backend=GoogleOAuth2,
#                 client_id=oauth2_settings.google_client_id,
#                 client_secret=oauth2_settings.google_client_secret,
#                 scope=["openid", "profile", "email"],
#                 claims=Claims(
#                     identity=lambda user: f"{user.provider}:{user.sub}",
#                 ),
#             ),
#             OAuth2Client(
#             backend=GithubOAuth2,
#             client_id=oauth2_settings.github_client_id,
#             client_secret=oauth2_settings.github_client_secret,
#             scope=["user:email"],
#             claims=Claims(
#                 picture="avatar_url",
#                 identity=lambda user: f"{user.provider}:{user.sub}",
#             ),
#         ),
#         ],
#     ),
# )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
