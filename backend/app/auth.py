
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .models import TokenOut, UserPublic
from .security import create_access_token, hash_password, verify_password
from .settings import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])

# OAuth2 scheme

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# In-memory single admin (dev)

def _get_admin_hash() -> str:
    s = get_settings()
    # Hash a la volee a partir du .env (dev)
    return hash_password(s.admin_password)


def _authenticate(email: str, password: str) -> UserPublic | None:
    s = get_settings()
    if email.lower() != s.admin_email.lower():
        return None
    if not verify_password(password, _get_admin_hash()):
        return None
    return UserPublic(email=s.admin_email)


@router.post("/token", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends()) -> TokenOut:  # noqa: B008
    user = _authenticate(form.username, form.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides.")
    token = create_access_token(sub=user.email)
    return TokenOut(access_token=token)


@router.get("/me", response_model=UserPublic)
def me(token: str = Depends(oauth2_scheme)) -> UserPublic:  # noqa: B008
    sub = None
    if token:
        sub = create_user_from_token(token)
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide ou expire.")
    return UserPublic(email=sub)


def create_user_from_token(token: str) -> str | None:
    from .security import decode_token

    return decode_token(token)
