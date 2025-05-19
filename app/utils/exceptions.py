from fastapi import HTTPException, status


class InvalidUsernameOrPasswordError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password"
        )


class TokenInBlackListError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is in blacklist")


class InvalidTokenError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")


class InvalidTokenTypeError(HTTPException):
    def __init__(self, token_type: str):
        detail = f"Token type is not '{token_type}'"
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UsernameIsTakenError(HTTPException):
    def __init__(self, username: str):
        detail = f"Username '{username}' is taken"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class RecordNotFound(HTTPException):
    def __init__(self, model: str = None, model_id: int = None):
        if model and model_id:
            detail = f"{model.capitalize()} record with {model.lower()}_id '{model_id}' not found"
        else:
            detail = "Not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class CustomDecodeError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
