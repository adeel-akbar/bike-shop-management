from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.oauth2 import create_access_token
from app.utils import verify_password

router = APIRouter(
    tags = ["login"]
)

@router.post("/login")
def login(
    admin: OAuth2PasswordRequestForm = Depends()  # noqa: B008
):
        password_check = verify_password(admin.password,settings.ADMIN_PASSWORD_HASH)
        if not password_check or admin.username != settings.ADMIN_USERNAME:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid Credentials",
                headers = {"WWW-Authenticate": "Bearer"}
            )
        access_token = create_access_token({"sub": settings.ADMIN_USERNAME})
        return {"access_token": access_token, "token_type": "bearer"}