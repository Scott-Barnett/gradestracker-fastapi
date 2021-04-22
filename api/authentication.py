from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional

from main import local_config


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
