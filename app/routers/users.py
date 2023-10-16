from typing import Annotated

from app.controllers.users import users_controller
from app.models.users import User as UserModel
from app.schemas.users import (
    User as UserSchema,
    UserCreate as UserCreateSchema,
    UserShow as UserShowSchema,
)
from app.schemas.tokens import Token
from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/", scheme_name="JWT")


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Registration",
    response_model=UserShowSchema,
)
async def register(user_schema: UserCreateSchema):
    return await users_controller.register(user_schema=user_schema)


@router.post(
    "/login/", response_model=Token, status_code=status.HTTP_200_OK, summary="Login"
)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await users_controller.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    access_token = users_controller.create_access_token(subject=user.username)
    refresh_token = users_controller.create_refresh_token(subject=user.username)
    response.set_cookie(key="access_token", value=f"{access_token}", httponly=True)
    response.set_cookie(key="refresh_token", value=f"{refresh_token}", httponly=True)
    return {
        "access_token": access_token,
    }


@router.get(
    "/users/me/",
    response_model=UserShowSchema,
    status_code=status.HTTP_200_OK,
    summary="Get user info",
)
async def current_user(token: str = Depends(oauth2_scheme)):
    return await users_controller.get_current_user(token=token)
