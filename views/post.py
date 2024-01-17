from fastapi import (
    Body,
    UploadFile,
    Form,
    HTTPException,
)
from fastapi.responses import JSONResponse
from models import *
from typing import Annotated
from fastapi import APIRouter


router = APIRouter()


@router.post("/auth/login/")
def login_form(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    """a simple form"""

    content = {"username": username, "password": password}
    return JSONResponse(content=content, status_code=200)


@router.post("/post/dummy/")
def post_dummy(
    model: TestModel
    | None = Body(example={"name": "string", "age": 18, "is_active": False})
) -> TestModel:
    """posting some fields to url (not saving)"""

    content = {"detail": model.__dict__}
    return JSONResponse(content=content, status_code=200)


@router.post("/post/uploadfile/")
def upload_file(file: UploadFile):
    """uploading files"""

    content = {"filename": file.filename}
    return JSONResponse(content=content, status_code=200)


@router.post("/handle/exeption/")
def handle_exeption(key: str):
    """handling some exeptions"""

    KEY_LIST = ["testkey", "testkey2", "testkey3"]

    if not key in KEY_LIST:
        return HTTPException(status_code=404, detail="Key Not Found")
    content = {"detail": "item found"}
    return JSONResponse(content=content, status_code=200)


FAKE_DB = {}


@router.post("/create/item/", status_code=201)
def create_item(model: Item):
    """creating an item in fake db"""

    global FAKE_DB
    try:
        id = list(FAKE_DB.keys())[-1] + 1
    except:
        id = 1
    FAKE_DB[id] = model.__dict__
    content = {"detail": FAKE_DB}
    return JSONResponse(content=content, status_code=201)
