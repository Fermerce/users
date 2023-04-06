import uuid
import typing as t
from fastapi import (
    status,
    Response,
)
from src.base.enum.sort_type import SortOrder

from src.base.schema.response import ITotalCount, ResponseMessage
from lib.errors import error
from src.app.products import schema, model
from src.app.products.Query import (
    product_query,
    product_attribute_query,
    product_property_query,
    product_media_query,
    variation_query,
)
from src.app.category.Query import category_query
from src.app.reviews.Query import review_query
from src.app.media_store.Query import media_query


async def create(data_in: schema.IProductIn) -> model.Product:
    check_product = await product_query.get_by_attr(
        attr=dict(name=data_in.name), first=True
    )
    if check_product:
        raise error.DuplicateError(f"Book with name `{data_in.name}`already  exists")
    pdf = None
    cover_img = None
    gallery_img = None
    if data_in.medias.pdf:
        pdf = await media_query.get(data_in.medias.pdf)
        if pdf:
            bad_type = media_query.check_file_type(file_type=["pdf"], media_objs=[pdf])
            if bad_type:
                raise error.BadDataError("Please upload a pdf file")

    if data_in.medias.cover_img:
        cover_img = await media_query.get(data_in.medias.cover_img)
        if cover_img:
            bad_type = media_query.check_file_type(
                file_type=media_query.allowed_image_extensions, media_objs=[cover_img]
            )
            if bad_type:
                raise error.BadDataError("Please upload a valid cover image file")

    if data_in.medias.gallery:
        gallery_img = await media_query.get_by_ids(data_in.medias.gallery)
        if gallery_img:
            bad_type = media_query.check_file_type(
                file_type=[
                    *media_query.allowed_image_extensions,
                    *media_query.allowed_video_extensions,
                ],
                media_objs=gallery_img,
            )
            if bad_type:
                raise error.BadDataError("Please upload a valid file for gallery")

    product_attribute = await product_attribute_query.create(
        obj=data_in.attribute.dict()
    )
    product_property = await product_property_query.create(obj=data_in.property.dict())
    product_category: t.List[str] = []
    if data_in.category:
        product_category = await category_query.get_by_props(
            prop_name="name", prop_values=data_in.category
        )

    product_media = await product_media_query.create_or_update(
        pdf=pdf if pdf else None,
        gallery=gallery_img if gallery_img else None,
        cover_img=cover_img if cover_img else None,
    )
    new_product = await product_query.create_product(
        obj=data_in,
        categories=product_category,
        attributes=product_attribute,
        properties=product_property,
        medias=product_media if product_media else None,
    )
    if new_product:
        return ResponseMessage(message="Book created successfully")
    raise error.ServerError("Error while creating product")


async def update(
    product_id: uuid.UUID,
    data_in: schema.IProductIn,
) -> model.Product:
    get_product = await product_query.get_by_attr(
        attr=dict(name=data_in.name), first=True, load_related=True
    )
    if get_product:
        if get_product.name == data_in.name and get_product.id != product_id:
            raise error.DuplicateError(f"Book with name `{data_in.name}`already  exist")
    if get_product:
        if get_product.id != product_id:
            get_product = await product_query.get(product_id, load_related=True)
    else:
        get_product = await product_query.get(product_id, load_related=True)
    if not get_product:
        raise error.NotFoundError("Book not found")

    pdf = None
    cover_img = None
    gallery_img = None
    if data_in.medias.pdf:
        if get_product.medias.pdf:
            if str(get_product.medias.pdf.id) != str(data_in.medias.pdf):
                pdf = await media_query.get(data_in.medias.pdf)
        if pdf:
            if pdf.id != get_product.medias.pdf.id:
                bad_type = media_query.check_file_type(
                    file_type=["pdf"], media_objs=[pdf]
                )
                if bad_type:
                    raise error.BadDataError("Please upload a pdf file")

    if data_in.medias.cover_img:
        if get_product.medias.cover_img:
            if str(data_in.medias.cover_img) != str(get_product.medias.cover_img.id):
                cover_img = await media_query.get(data_in.medias.cover_img)
        if cover_img:
            bad_type = media_query.check_file_type(
                file_type=media_query.allowed_image_extensions,
                media_objs=[cover_img],
            )
            if bad_type:
                raise error.BadDataError("Please upload a valid cover image file")

    if data_in.medias.gallery:
        for media in get_product.medias.gallery:
            if media.id in data_in.medias.gallery:
                data_in.medias.gallery.remove(media.id)

        if len(data_in.medias.gallery) > 0:
            gallery_img = await media_query.get_by_ids(data_in.medias.gallery)
            if gallery_img:
                bad_type = media_query.check_file_type(
                    file_type=[
                        *media_query.allowed_image_extensions,
                        *media_query.allowed_video_extensions,
                    ],
                    media_objs=gallery_img,
                )
                if bad_type:
                    raise error.BadDataError("Please upload a valid file for gallery")

    product_category: t.List[str] = []
    if data_in.category:
        for category in get_product.categories:
            if category.name in data_in.category:
                data_in.category.remove(category.name)
        if len(data_in.category) > 0:
            product_category = await category_query.get_by_names(data_in.category)
    if data_in.attribute.dict() != dict(**get_product.attribute.__dict__):
        await product_attribute_query.update(
            get_product.attribute.id, data_in.attribute
        )

    if data_in.property.dict() != dict(**get_product.property.__dict__):
        await product_property_query.update(get_product.property.id, data_in.property)
    await product_media_query.create_or_update(
        product_id=get_product.id,
        gallery=gallery_img if gallery_img else None,
        pdf=pdf if pdf else None,
        cover_img=cover_img if cover_img else None,
    )

    result = await product_query.update_product(
        obj=data_in,
        product=get_product,
        categories=product_category,
    )
    if result:
        return get_product
    raise error.ServerError("Error while updating Book details")


async def get(
    product_id: uuid.UUID,
    slug: str,
) -> model.Product:
    get_product = None
    if product_id and not slug:
        get_product = await product_query.get(product_id, load_related=True)

    elif slug and not product_id:
        get_product = await product_query.get_by_attr(
            attr=dict(slug=slug), first=True, load_related=True
        )
    elif product_id and slug:
        get_product = await product_query.get(product_id, load_related=True)
    else:
        raise error.BadDataError("Either Book id or slug is required")
    if not get_product:
        raise error.NotFoundError("Book not found")
    return get_product


async def filter(
    filter: str = "",
    page_size: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
    is_series: bool = False,
    is_active: bool = True,
    is_assigned: bool = False,
    load_related: bool = False,
) -> t.List[model.Product]:
    to_search = dict()
    if is_active:
        to_search["is_active"] = is_active
    if is_series:
        to_search["is_series"] = is_series
    if is_assigned:
        if is_assigned:
            to_search["is_assigned"] = is_assigned
        else:
            to_search["is_series"] = False
            to_search["is_assigned"] = False
    if not is_series and not is_assigned:
        to_search["is_series"] = False
        to_search["is_assigned"] = False

    get_product = await product_query.filter(
        filter_string=filter,
        page_size=page_size,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
        strict_search=to_search,
        load_related=load_related,
    )
    return get_product


async def get_product_review_count(
    product_id: uuid.UUID,
) -> ITotalCount:
    product_review = await review_query.get_by_attr(attr=dict(product_id=product_id))
    return ITotalCount(count=len(product_review))


async def get_product_count() -> ITotalCount:
    total = await product_query.get_count()
    return ITotalCount(count=total)


async def get_product_variations(
    product_id: uuid.UUID,
) -> ResponseMessage:
    get_variations = await product_query.get_by_attr(
        attr=dict(parent_id=product_id), load_related=True, expunge=False
    )
    return get_variations


async def add_product_variation(
    data_in: schema.IVariationProductIn,
) -> ResponseMessage:
    check_product = await product_query.get(id=data_in.product_id, expunge=False)
    if not check_product:
        raise error.NotFoundError("Book is not found")
    check_variation = await variation_query.get(id=data_in.variation_id)
    if not check_variation:
        raise error.NotFoundError("series is not found")
    if check_variation.parent_id == check_product.id or check_variation.is_assigned:
        raise error.DuplicateError("series is already part of this product")
    update_variation = await variation_query.update(
        id=data_in.variation_id,
        obj=dict(parent_id=data_in.product_id, is_assigned=True),
    )
    update_product = await product_query.update(
        id=check_product.id, obj=dict(is_series=True)
    )
    if update_product and update_variation:
        return ResponseMessage(message="series added successfully")
    raise error.BadDataError("Error adding series to product")


async def remove_product_variation(data_in: schema.IVariationProductIn):
    get_product = await product_query.get(id=data_in.product_id)
    if not get_product:
        raise error.NotFoundError("Book is not found")
    get_variation = await variation_query.get(id=data_in.variation_id)
    if not get_variation:
        raise error.NotFoundError("series is not found")
    if get_variation.parent_id != get_product.id:
        raise error.BadDataError("series is not part of this product")
    remove_variation = await variation_query.remove_variation(obj=data_in)
    if remove_variation:
        update_product = await product_query.update(
            id=get_product.id, obj=dict(is_series=False)
        )
        if update_product:
            return ResponseMessage(message="series removed successfully")
    raise error.BadDataError("Error removing series from Book")


async def get_product_review_average(product_id: uuid.UUID) -> int:
    product_review = await review_query.get(id=product_id)
    if not product_review:
        raise error.NotFoundError("Book not found")
    result = review_query.get_average_rating(id=product_review.product)
    return ITotalCount(count=result)


async def delete(product_id: str):
    get_product = await product_query.get(product_id)
    if not get_product:
        raise error.NotFoundError("Book not found")
    await product_query.delete(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
