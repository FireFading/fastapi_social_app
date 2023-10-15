from typing import Annotated

from app.controllers.users import users_controller
from app.models.users import User as UserModel
from app.schemas.users import User as UserSchema, UserCreate as UserCreateSchema
from app.schemas.tokens import Token
from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Registration",
)
async def register(user_schema: UserCreateSchema):
    await users_controller.register(user_schema=user_schema)
    return {"email": user_schema.email, "detail": "User created"}


@router.post(
    "/token", response_model=Token, status_code=status.HTTP_200_OK, summary="Login"
)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await users_controller.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    access_token = users_controller.create_access_token(data={"sub": user.username})
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/users/me/", response_model=None, status_code=status.HTTP_200_OK, summary="Get current user")
# async def current_user(current_user: Annotated[UserModel, Depends(users_controller.get_current_active_user)]):
#     return current_user


# @router.get("/users/me/items/")
# async def about_user(current_user: Annotated[UserModel, Depends(users_controller.get_current_active_user)]):
#     return [{"item_id": "Foo", "owner": current_user.username}]
