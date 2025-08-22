import datetime as dt

from jose import JWTError, jwt
from passlib.context import CryptContext

from .settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(sub: str) -> str:
    s = get_settings()
    now = dt.datetime.utcnow()
    exp = now + dt.timedelta(minutes=s.jwt_exp_min)
    payload = {"sub": sub, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, s.jwt_secret, algorithm=s.jwt_alg)


def decode_token(token: str) -> str | None:
    s = get_settings()
    try:
        payload = jwt.decode(token, s.jwt_secret, algorithms=[s.jwt_alg])
        return str(payload.get("sub"))
    except JWTError:
        return None
