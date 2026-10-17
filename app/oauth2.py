from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")
def create_access_token(payload: dict):
    copy_of_payload = payload.copy()
    exp = datetime.now(UTC) + timedelta(minutes = settings.TOKEN_EXPIRATION_TIME)
    copy_of_payload.update({"exp": exp})
    access_token = jwt.encode(copy_of_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return access_token

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_error = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[
            settings.ALGORITHM
        ], options = {"require": ["sub", "exp"]})
        current_user = decoded_token.get("sub")
        if current_user != settings.ADMIN_USERNAME:
            raise credentials_error
    except jwt.InvalidTokenError:
        raise credentials_error
    return current_user