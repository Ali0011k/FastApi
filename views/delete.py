from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from views.post import FAKE_DB


router = APIRouter()


@router.delete("/delete/{item_id}/")
async def delete_item(item_id: int):
    """delete item from fake db"""

    global FAKE_DB
    FAKE_DB.pop(item_id)
    content = {"detail": "item deleted"}
    return JSONResponse(content=content, status_code=status.HTTP_204_NO_CONTENT)
