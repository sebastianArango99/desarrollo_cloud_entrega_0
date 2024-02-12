from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)  # Token expires after 15 minutes
    to_encode.update({"exp": expire})
    token = encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return token

def validate_token(token: str) -> dict:
    try:
        data = decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")
