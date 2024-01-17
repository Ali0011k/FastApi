from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from auth.jwt import decode_jwt
from databases.sqlite import SessionLocal
from databases.sqlite import User


class JWTBearer(HTTPBearer):
    """a jwt authentication to for fast api"""

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if not credentials.scheme == "Bearer":
            raise HTTPException(401, "token type is invalid")
        if not self.validate_jwt(credentials.credentials):
            raise HTTPException(401, "you dont have access to this page")

    def validate_jwt(self, jwtcode: str) -> bool:
        """validate jwt"""

        is_token_valid: bool = False
        user_id = decode_jwt(jwtcode)

        if user_id is not None:
            db = SessionLocal()
            user = db.query(User).filter(User.id == user_id).first()
            if user is not None and user.is_active == True:
                is_token_valid = True
        else:
            is_token_valid = False

        return is_token_valid
