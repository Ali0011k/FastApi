from fastapi import (
    Depends,
    Form,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from sqlalchemy.orm import Session
from databases.sqlite import SessionLocal
from databases.sqlite import User as DBUSER
from auth.jwt import encode_jwt
from fastapi import APIRouter
from utils.hashers import verify_password

router = APIRouter()


# Dependency to open database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/auth/token/access/")
async def access_token(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    """generate access token for user"""

    USER = db.query(DBUSER).filter(DBUSER.username == username).first()

    if USER is not None:
        if verify_password(password, USER.password):
            token = encode_jwt(jsonable_encoder(USER))
            content = {"token": token}
            return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    content = {"detail": "can't generate token for this informations"}
    return JSONResponse(content=content, status_code=status.HTTP_401_UNAUTHORIZED)
