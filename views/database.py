from fastapi import (
    Body,
    Depends,
    Form,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import *
from models import User as MODELUSER
from sqlalchemy.orm import Session
from databases.sqlite import SessionLocal
from databases.sqlite import User as DBUSER
from fastapi import APIRouter
from utils.hashers import hash_password, verify_password

router = APIRouter()


# Dependency to open database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/database/users/",
)
def all_users(db: Session = Depends(get_db)):
    """get all users from data base"""

    users = db.query(DBUSER).all()
    return_object = []
    for user in users:
        safe_user = SafeUser(**user.__dict__)
        return_object.append(safe_user)
    content = jsonable_encoder(return_object)
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@router.get(
    "/database/users/{id}/",
    status_code=200,
)
def get_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(DBUSER).filter(DBUSER.id == id).first()
        if user is None:
            content = {"detail": "Not Found"}
            return JSONResponse(content=content, status_code=status.HTTP_404_NOT_FOUND)

        user = SafeUser(**user.__dict__)
        content = jsonable_encoder(user)
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    except:
        content = {"detail": "Not Found"}
        return JSONResponse(content=content, status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    "/database/users/",
    status_code=201,
)
def create_user(
    model: MODELUSER
    | None = Body(
        example={
            "first_name": "string",
            "last_name": "string",
            "password": "string",
            "email": "string",
            "id": 1,
            "username": "string",
            "is_active": True,
        }
    ),
    db: Session = Depends(get_db),
):
    """create a new user in database"""

    db_user = DBUSER(**model.__dict__)
    db_user.password = hash_password(db_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return_object = SafeUser(**db_user.__dict__)
    content = {"user": jsonable_encoder(return_object)}
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)


@router.put(
    "/database/users/{id}/",
)
def update_user(model: MODELUSER, id: int, db: Session = Depends(get_db)):
    """update all user fields in db"""

    user = db.query(DBUSER).filter(DBUSER.id == id).first()

    if not user:
        content = {"detail": "Not Found"}
        return JSONResponse(content=content, status_code=status.HTTP_404_NOT_FOUND)

    REQUIRED_FIELDS = []
    for key, value in model.__dict__.items():
        if value is None:
            REQUIRED_FIELDS.routerend(key)
        else:
            if key == "password":
                value = hash_password(value)
            setattr(user, key, value)

    if REQUIRED_FIELDS.__len__() > 0:
        content = {}
        for key in REQUIRED_FIELDS:
            content[f"{key}"] = f"you must enetr required field : {key}"
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    db.commit()
    db.refresh(user)
    return_object = SafeUser(**user.__dict__)
    content = jsonable_encoder(return_object)
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@router.patch("/database/users/{id}/")
def partial_update_user(
    id: int, model: MODELUSER = None, db: Session = Depends(get_db)
):
    """partial update for user model"""

    user = db.query(DBUSER).filter(DBUSER.id == id).first()

    if not user:
        content = {"detail": "Not Found"}
        return JSONResponse(content=content, status_code=status.HTTP_404_NOT_FOUND)

    for key, value in model.__dict__.items():
        if value is not None:
            if key == "password":
                value = hash_password(value)
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return_object = SafeUser(**user.__dict__)
    content = jsonable_encoder(return_object)
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@router.delete(
    "/database/users/{id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(id: int, db: Session = Depends(get_db)):
    """delete user"""

    user = db.query(DBUSER).filter(DBUSER.id == id).first()

    if not user:
        content = {"detail": "Not Found"}
        return JSONResponse(content=content, status_code=status.HTTP_404_NOT_FOUND)

    db.delete(user)
    db.commit()

    content = {"detail": "user deleted"}
    return JSONResponse(content=content, status_code=status.HTTP_204_NO_CONTENT)
