from fastapi import status
from fastapi.responses import JSONResponse
from models import *
from fastapi import APIRouter
from views.post import FAKE_DB

router = APIRouter()


@router.patch("/update/partial/{item_id}/")
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
