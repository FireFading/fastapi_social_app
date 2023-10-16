from fastapi import HTTPException, status


class UserExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InsufficientCredentialsException(HTTPException):
    def __init__(self):
        super().__init(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Insufficient credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InactiveUserException(HTTPException):
    def __init__(self):
        super().__init(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
