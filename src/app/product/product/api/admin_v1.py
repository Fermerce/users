import uuid
from fastapi import APIRouter, status

from src.app.product import schema, service
from src.base.schema.response import ResponseMessage


router = APIRouter(prefix="/ad/products", tags=["products"])
variation = APIRouter(prefix="/variations", tags=["products"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(data_in: schema.IProductIn):
    return await service.create(
        data_in=data_in,
    )


@router.put("/{product_id}", status_code=status.HTTP_201_CREATED)
async def update_product(product_id: uuid.UUID, data_in: schema.IProductIn):
    return await service.update(
        product_id=product_id,
        data_in=data_in,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: uuid.UUID) -> None:
    return await service.delete(product_id=product_id)


@variation.put("/", status_code=status.HTTP_200_OK)
async def add_product_to_variation(
    data_in: schema.IVariationProductIn,
):
    return await service.add_product_variation(data_in)


@variation.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_variation(
    product_id: uuid.UUID,
):
    return await service.get_product_variations(product_id)


@variation.delete("/", status_code=status.HTTP_200_OK)
async def remove_product_from_variation(
    data_in: schema.IVariationProductIn,
) -> ResponseMessage:
    return await service.remove_product_variation(data_in)


@router.get("/{product_id}/reviews/count", status_code=status.HTTP_200_OK)
async def get_product_review_count(product_id: uuid.UUID):
    return await service.get_product_review_count(product_id=product_id)


@router.get("/{product_id}/reviews/average", status_code=status.HTTP_200_OK)
async def get_product_average_review(product_id: uuid.UUID):
    return await service.get_product_review_count(product_id=product_id)


@router.get(
    "/count",
    status_code=status.HTTP_200_OK,
)
async def get_product_count():
    return await service.get_product_count()
