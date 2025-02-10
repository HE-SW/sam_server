from fastapi import APIRouter, Depends, Response
from dependency_injector.wiring import inject, Provide

from container.ai.container import AiContainer
from service.ai import AiService


ai_router: APIRouter = APIRouter()

@ai_router.get("/get_sam_npy/image_path")
@inject
async def get_npy_by_img_path(
    image_url:str,
    service: AiService = Depends(Provide[AiContainer.ai_service]),
):  
    npy_bytes = service.get_npy_bytes_by_image_path(image_path=image_url)
    filename = image_url.replace('.jpg', '.npy') if image_url.endswith('.jpg') else "embedding.npy"

    return Response(
        content=npy_bytes,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@ai_router.get("/get_sam_npy/base64")
@inject
async def get_npy_by_base64(
    service: AiService = Depends(Provide[AiContainer.ai_service]),
):
    return Response(
        content=''
    )