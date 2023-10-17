from fastapi import HTTPException, status


class NotAllowedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to access this resource",
        )
