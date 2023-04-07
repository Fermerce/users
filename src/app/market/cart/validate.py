from src.app.products.model import Product, ProductProperty
from src.lib.errors import error
from src.app.cart import schema


async def validate_cart_data_on_create(
    data_in: schema.ICartIn, product: Product
) -> None:
    if not product:
        raise error.NotFoundError("Product not found")

    if (
        data_in.hard_back_qty > 0
        and product.property.hard_back_qty == 0
        and data_in.paper_back_qty > 0
        and product.property.paper_back_qty == 0
        and product.property.has_pdf != data_in.pdf
    ):
        raise error.BadDataError(
            f"`{product.name}` is out of stock, please check back later"
        )

    if data_in.hard_back_qty > 0:
        if (
            data_in.hard_back_qty > product.property.hard_back_qty
            and product.property.hard_back_qty != 0
        ):
            raise error.BadDataError(
                f"Only {product.property.hard_back_qty} of `{product.name}`left"
            )
        elif product.property.hard_back_qty == 0:
            raise error.BadDataError(
                f"Hard back of `{product.name}` is out of stock, please check later"
            )
    if data_in.paper_back_qty > 0:
        if (
            data_in.paper_back_qty > product.property.paper_back_qty
            and product.property.paper_back_qty != 0
        ):
            raise error.BadDataError(
                f"Only {product.property.paper_back_qty} of `{product.name}`left"
            )
        if product.property.paper_back_qty == 0:
            raise error.BadDataError(
                f"Paper back of `{product.name}` is out of stock, please check later"
            )

    if data_in.pdf and not product.property.has_pdf:
        raise error.BadDataError(f"Pdf of `{product.name}` is not available")


async def validate_cart_data_on_update(
    data_in: schema.ICartIn, property: ProductProperty
):
    if (
        data_in.hard_back_qty > 0
        and property.hard_back_qty == 0
        and data_in.paper_back_qty > 0
        and property.paper_back_qty == 0
        and property.has_pdf != data_in.pdf
    ):
        raise error.BadDataError(
            f"`{property.name}` is out of stock, please check back later"
        )

    if data_in.hard_back_qty > 0:
        if (
            data_in.hard_back_qty > property.hard_back_qty
            and property.hard_back_qty != 0
        ):
            raise error.BadDataError(
                f"Only {property.hard_back_qty} of `{property.name}` left"
            )
        elif property.hard_back_qty == 0:
            raise error.BadDataError(
                f"Hard back of `{property.name}` is out of stock, please check later"
            )
    if data_in.paper_back_qty > 0:
        if (
            data_in.paper_back_qty > property.paper_back_qty
            and property.paper_back_qty != 0
        ):
            raise error.BadDataError(
                f"Only {property.paper_back_qty} of `{property.name}` left"
            )
        elif property.paper_back_qty == 0:
            raise error.BadDataError(
                f"Paper back of `{property.name}` is out of stock, please check later"
            )

    if data_in.pdf and not property.has_pdf:
        raise error.BadDataError(f"Pdf of `{property.name}` is not available")
