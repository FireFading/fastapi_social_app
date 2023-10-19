from app.config import oauth2_scheme
from app.controllers.users import users_controller
from app.schemas.tokens import Token
from app.schemas.users import ResetPassword as ResetPasswordSchema
from app.schemas.users import UpdatePassword as UpdatePasswordSchema
from app.schemas.users import UserCreate as UserCreateSchema
from app.schemas.users import UserEmail as UserEmailSchema
from app.schemas.users import UserShow as UserShowSchema
from app.schemas.users import UserUpdate as UserUpdateSchema
from app.utils.mail import html_reset_password_mail, send_mail
from fastapi import APIRouter, Depends, Response, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})


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
    username = form_data.username
    await users_controller.authenticate_user(username=username, password=form_data.password)
    access_token = users_controller.create_token(subject=username)
    refresh_token = users_controller.create_token(subject=username, token_type="refresh")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return {
        "access_token": access_token,
    }


@router.delete("/logout/", status_code=status.HTTP_200_OK, summary="Logout")
async def logout(response: Response, token: str = Depends(oauth2_scheme)):
    await users_controller.verify_token(token=token)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"detail": "logout"}


@router.post(
    "/change-password/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Change password",
)
async def change_password(data: UpdatePasswordSchema, token: str = Depends(oauth2_scheme)):
    user = await users_controller.verify_token(token=token)
    await users_controller.change_password(user=user, data=data)
    return {"detail": "password updated"}


@router.post(
    "/forgot-password/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Send requests for reset password token mail",
)
async def forgot_password(data: UserEmailSchema):
    email = data.email
    await users_controller.get_user_or_404(email=email)
    reset_password_token = users_controller.create_token(subject=email, token_type="reset")
    subject = "Reset password"
    recipients = [email]
    body = html_reset_password_mail(reset_password_token=reset_password_token)
    await send_mail(subject=subject, recipients=recipients, body=body)
    return {"detail": "reset token sent"}


@router.post(
    "/reset-password/{token}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Reset password",
)
async def reset_password(
    token: str,
    data: ResetPasswordSchema,
):
    await users_controller.reset_password(token=token, data=data)
    return {"detail": "password reset"}


@router.post(
    "/refresh-token/",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
)
async def refresh_token(response: Response, refresh_token: str):
    user = await users_controller.verify_token(token=refresh_token, token_type="refresh")
    access_token = users_controller.create_token(subject=user.username)
    new_refresh_token = users_controller.create_token(subject=user.username, token_type="refresh")

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


@router.get(
    "/search/{data}",
    response_model=list[UserShowSchema],
    status_code=status.HTTP_200_OK,
    summary="Search users",
)
async def search_users(data: str, token: str = Depends(oauth2_scheme)):
    await users_controller.verify_token(token=token)
    return await users_controller.search_users(data=data)


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


@router.post("/avatar/", status_code=status.HTTP_200_OK, summary="Update User Avatar")
async def update_user_avatar(photo: UploadFile, token: str = Depends(oauth2_scheme)):
    current_user = await users_controller.verify_token(token=token)
    await users_controller.update_avatar(user=current_user, photo=photo)
    return {"detail": "photo uploaded"}


@router.get("/avatar/", status_code=status.HTTP_200_OK, summary="Get User Avatar")
async def get_avatar(token: str = Depends(oauth2_scheme)):
    current_user = await users_controller.verify_token(token=token)
    avatar = users_controller.get_avatar(user=current_user)
    return FileResponse(avatar) if avatar else {"detail": "no avatar"}


@router.delete("/avatar/", status_code=status.HTTP_200_OK, summary="Delete User Avatar")
async def delete_avatar(token: str = Depends(oauth2_scheme)):
    current_user = await users_controller.verify_token(token=token)
    users_controller.delete_avatar(user=current_user)
    return {"detail": "photo deleted"}
