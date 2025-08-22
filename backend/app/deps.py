from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .db import get_db
from .security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def require_auth(token: str = Depends(oauth2_scheme)) -> str:  # noqa: B008
    sub = decode_token(token) if token else None
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expire.",
        )
    return sub


def get_db_dep(db: Session = Depends(get_db)) -> Session:  # noqa: B008
    return db

