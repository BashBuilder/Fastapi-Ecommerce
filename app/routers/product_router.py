from fastapi import APIRouter

router = APIRouter(tags=["Product"], prefix="product")


@router.post("/upload-image/{id}")
async def upload_product_image():
  pass
