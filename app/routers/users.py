from app.controllers.users import users_controller
from app.schemas.tokens import Token
from app.schemas.users import UserCreate as UserCreateSchema
from app.schemas.users import UserShow as UserShowSchema
from app.schemas.users import UserUpdate as UserUpdateSchema
from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/", scheme_name="JWT")


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Registration",
    response_model=UserShowSchema,
)
async def register(user_schema: UserCreateSchema):
    return await users_controller.register(user_schema=user_schema)


@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK, summary="Login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await users_controller.authenticate_user(username=form_data.username, password=form_data.password)
    access_token = users_controller.create_token(subject=user.username)
    refresh_token = users_controller.create_token(subject=user.username, token_type="refresh")
    response.set_cookie(key="access_token", value=f"{access_token}", httponly=True)
    response.set_cookie(key="refresh_token", value=f"{refresh_token}", httponly=True)
    return {
        "access_token": access_token,
    }


@router.post(
    "/refresh-token/",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
)
async def refresh_token(response: Response, refresh_token: str):
    user = await users_controller.verify_token(token=refresh_token, token_type="refresh")
    access_token = users_controller.create_access_token(subject=user.username)
    new_refresh_token = users_controller.create_refresh_token(subject=user.username, token_type="refresh")

    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True)

    return {
        "access_token": access_token,
    }


@router.get(
    "/me/",
    response_model=UserShowSchema,
    status_code=status.HTTP_200_OK,
    summary="Get user info",
)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return await users_controller.verify_token(token=token)


@router.put(
    "/update/",
    response_model=UserShowSchema,
    status_code=status.HTTP_200_OK,
    summary="Update User Info",
)
async def update_user_info(
    user_update: UserUpdateSchema,
    token: str = Depends(oauth2_scheme),
):
    current_user = await users_controller.verify_token(token=token)
    return await users_controller.update_user_info(user=current_user, update_user_schema=user_update)
