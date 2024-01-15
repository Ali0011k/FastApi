from fastapi import (
    FastAPI,
    Query,
    Path,
    Body,
    Cookie,
    Header,
    Depends,
    UploadFile,
    Form,
    HTTPException,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import *
from models import User as MODELUSER
from typing import Annotated
from jose import jwt
from sqlalchemy.orm import Session
from databases.sqlite import Base, engine, SessionLocal
from databases.sqlite import User as DBUSER

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/", tags=["get requests"])
def root():
    """returns a hello word for this url"""

    content = {"hello": "world"}
    return JSONResponse(content=content, status_code=200)


@app.get("/params/{something}/", tags=["get requests"])
def params(something: int, q: bool = None):
    """add an int to path params (!important) like this : params/1/ and add an qury params in url like this : params/1/?q=1(true)(!not imporant)"""

    content = {"pathparams": something, "queryparams": q}
    return JSONResponse(content=content, status_code=200)


@app.get("/query/params/", tags=["get requests"])
def query_params(q: int = Query(description="query parmas")):
    """returning query paramter"""

    content = {"page": "/query/params/"}
    if q:
        content.update({"q": q})
    print(q)
    return JSONResponse(content=content, status_code=200)


@app.get("/path/params/{item_id}/", tags=["get requests"])
def path_params(item_id: int = Path(description="path parmas")):
    """returning path paramter"""

    content = {"page": "/path/params/", "item_id": item_id}
    return JSONResponse(content=content, status_code=200)


@app.get("/path/cookie/params/", tags=["get requests"])
def cookie_params(q: Annotated[str | None, Cookie()]):
    """adding cookie params"""

    content = {"param": q}
    return JSONResponse(content=content, status_code=200)


@app.get("/path/header/params/", tags=["get requests"])
def header_params(q: Annotated[str | None, Header()]):
    """adding header params"""

    content = {"param": q}
    return JSONResponse(content=content, status_code=200)


@app.post("/auth/login/", tags=["post requests"])
def login_form(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    """a simple form"""

    content = {"username": username, "password": password}
    return JSONResponse(content=content, status_code=200)


@app.post("/post/dummy/", tags=["post requests"])
def post_dummy(
    model: TestModel
    | None = Body(example={"name": "string", "age": 18, "is_active": False})
) -> TestModel:
    """posting some fields to url (not saving)"""

    content = {"detail": model.__dict__}
    return JSONResponse(content=content, status_code=200)


@app.post("/post/uploadfile/", tags=["post requests"])
def upload_file(file: UploadFile):
    """uploading files"""

    content = {"filename": file.filename}
    return JSONResponse(content=content, status_code=200)


@app.post("/handle/exeption/", tags=["post requests"])
def handle_exeption(key: str):
    """handling some exeptions"""

    KEY_LIST = ["testkey", "testkey2", "testkey3"]

    if not key in KEY_LIST:
        return HTTPException(status_code=404, detail="Key Not Found")
    content = {"detail": "item found"}
    return JSONResponse(content=content, status_code=200)


FAKE_DB = {}


@app.post("/create/item/", status_code=201, tags=["post requests"])
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


@app.put("/update/item/{item_id}/", tags=["put requests"])
def update_item(item_id: int, model: Item):
    """update an item with item id"""

    global FAKE_DB

    KEY_LIST = list(FAKE_DB.keys())
    if item_id in KEY_LIST:
        stored_data = Item(**model.__dict__)
        if model.name is not None and model.price is not None:
            FAKE_DB[item_id] = stored_data.__dict__
        else:
            content = {"detail": "fields are required in this typr of update"}
            return JSONResponse(content=content, status_code=400)
        content = {"detail": FAKE_DB[item_id]}
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    content = {"detail": "NOT FOUND"}
    return JSONResponse(content=content, status_code=status.HTTP_404_NOT_FOUND)


@app.patch("/update/partial/{item_id}/", tags=["patch requests"])
def partial_update_item(item_id: int, model: Item):
    """add partial update to item model"""

    global FAKE_DB

    KEY_LIST = list(FAKE_DB.keys())
    if item_id in KEY_LIST:
        last_item = FAKE_DB[item_id]
        stored_model = Item(**last_item)
        update_data = model.dict(exclude_unset=True)
        new_item = stored_model.copy(update=update_data)
        FAKE_DB[item_id] = new_item.dict()

        content = {"detail": FAKE_DB[item_id]}
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    content = {"detail": "NOT FOUND"}
    return JSONResponse(content=content, status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/delete/{item_id}/", tags=["delete requests"])
def delete_item(item_id: int):
    """delete item from fake db"""

    global FAKE_DB
    FAKE_DB.pop(item_id)
    content = {"detail": "item deleted"}
    return JSONResponse(content=content, status_code=status.HTTP_204_NO_CONTENT)


USER = {
    "username": "ali",
    "password": "ali2",
    "id": 1,
}


@app.post("/auth/token/access/fake/", tags=["jwt"])
def fake_access_token(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    """generate access token for fake user"""

    global USER
    if username == USER["username"] and password == USER["password"]:
        token = jwt.encode(
            USER,
            "mysecretkey",
            "HS256",
            {
                "typ": "access",
            },
        )
        content = {"token": token}
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    content = {"detail": "can't generate token for this informations"}
    return JSONResponse(content=content, status_code=status.HTTP_401_UNAUTHORIZED)


# Dependency to open database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/database/users/", tags=["database"])
def all_users(db: Session = Depends(get_db)):
    """get all users from data base"""

    users = db.query(DBUSER).all()
    content = {"users": jsonable_encoder(users)}
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@app.get("/database/users/{id}/", tags=["database"], status_code=200)
def get_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(DBUSER).filter(DBUSER.id == id).first()
        content = jsonable_encoder(user)
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    except:
        content = {"detail": "Not Found"}
        return JSONResponse(content=content, status_code=status.HTTP_404_NOT_FOUND)


@app.post("/database/users/", tags=["database"], status_code=201)
def create_user(
    model: MODELUSER
    | None = Body(
        example={
            "id": 0,
            "first_name": "string",
            "last_name": "string",
            "email": "string",
            "password": "string",
            "is_active": True,
            "items": [],
        }
    ),
    db: Session = Depends(get_db),
):
    """create a new user in database"""

    db_user = DBUSER(**model.__dict__)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    content = {"user": jsonable_encoder(db_user)}
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)


@app.put("/database/users/{id}/", tags=["database"])
def update_user(model: MODELUSER, id: int, db: Session = Depends(get_db)):
    """update all user fields in db"""

    user = db.query(DBUSER).filter(DBUSER.id == id).first()

    if not user:
        content = {"detail": "Not Found"}
        return JSONResponse(content=content, status_code=status.HTTP_404_NOT_FOUND)

    REQUIRED_FIELDS = []
    for key, value in model.__dict__.items():
        if value is None:
            REQUIRED_FIELDS.append(key)
        else:
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
    content = jsonable_encoder(user)
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@app.patch("/database/users/{id}/", tags=["database"])
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
            setattr(user, key, value)

    db.commit()
    db.refresh(user)

    content = jsonable_encoder(user)
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@app.delete("/database/users/{id}/", tags=["database"])
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", reload=True)
