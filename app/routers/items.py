from fastapi import APIRouter, Depends
from app.dependencies import common_dependency

router = APIRouter()

@router.get("/")
async def get_items(dep=Depends(common_dependency)):
    return {"items": ["item1", "item2"], "dependency": dep}
