from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "meusegredoseguro123"
ALGORITHM = "HS256"

def create_reset_password_token(email: str, expires_delta: timedelta = timedelta(minutes=30)):
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_password_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None
