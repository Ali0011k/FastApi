from fastapi import (
    Query,
    Path,
    Cookie,
    Header,
)
from fastapi.responses import JSONResponse
from models import *
from typing import Annotated
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """returns a hello word for this url"""

    content = {"hello": "world"}
    return JSONResponse(content=content, status_code=200)


@router.get("/params/{something}/")
async def params(something: int, q: bool = None):
    """add an int to path params (!important) like this : params/1/ and add an qury params in url like this : params/1/?q=1(true)(!not imporant)"""

    content = {"pathparams": something, "queryparams": q}
    return JSONResponse(content=content, status_code=200)


@router.get("/query/params/")
async def query_params(q: int = Query(description="query parmas")):
    """returning query paramter"""

    content = {"page": "/query/params/"}
    if q:
        content.update({"q": q})
    print(q)
    return JSONResponse(content=content, status_code=200)


@router.get("/path/params/{item_id}/")
async def path_params(item_id: int = Path(description="path parmas")):
    """returning path paramter"""

    content = {"page": "/path/params/", "item_id": item_id}
    return JSONResponse(content=content, status_code=200)


@router.get("/path/cookie/params/")
async def cookie_params(q: Annotated[str | None, Cookie()]):
    """adding cookie params"""

    content = {"param": q}
    return JSONResponse(content=content, status_code=200)


@router.get("/path/header/params/")
async def header_params(q: Annotated[str | None, Header()]):
    """adding header params"""

    content = {"param": q}
    return JSONResponse(content=content, status_code=200)
