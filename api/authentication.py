from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional

from local_config import local_config


class TokenManager:
    @staticmethod
    def generate_token(username: str, minutes_active: Optional[int] = None) -> str:
        if minutes_active is None:
            minutes_active = local_config["TOKEN_MANAGER"]["DEFAULT_MINUTES_ACTIVE"]
        expiry = datetime.utcnow() + timedelta(minutes=minutes_active)
        return jwt.encode(
            {"sub": username, "exp": expiry},
            local_config["TOKEN_MANAGER"]["SECRET_KEY"],
            algorithm=local_config["TOKEN_MANAGER"]["ALGORITHM"]
        )

    @staticmethod
    def validate_token(token: str) -> Optional[str]:
        try:
            decoded = jwt.decode(
                token,
                local_config["TOKEN_MANAGER"]["SECRET_KEY"],
                algorithms=local_config["TOKEN_MANAGER"]["ALGORITHM"]
            )
            return decoded["sub"]
        except JWTError:
            return None


class PasswordManager:
    PW_CONTEXT = CryptContext(schemes=[local_config["PASSWORD_MANAGER"]["HASH_SCHEME"]], deprecated=["auto"])

    @staticmethod
    def hash_password(password: str) -> str:
        return PasswordManager.PW_CONTEXT.hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return PasswordManager.PW_CONTEXT.verify(password, password_hash)
