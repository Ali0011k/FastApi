from fastapi import status
from fastapi.responses import JSONResponse
from models import *
from fastapi import APIRouter
from views.post import FAKE_DB


router = APIRouter()


@router.put("/update/item/{item_id}/")
async def update_item(item_id: int, model: Item):
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
