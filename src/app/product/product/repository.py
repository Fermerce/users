import typing as t
from uuid import UUID

from pydantic import BaseModel

from src.app.category.model import Category
from src.lib.errors import error

from src.base.repository.base_repository import BaseRepository
from src.app.product import model, schema


class ProductAttributeRepository(BaseRepository[model.ProductAttribute,]):
    def __init__(self):
        super().__init__(model.ProductAttribute)


class ProductPropertyRepository(BaseRepository[model.ProductProperty]):
    def __init__(self):
        super().__init__(model.ProductProperty)

    async def update_quantity(
        self,
        hard_back_qty: int,
        paper_back_qty: int,
        property_id: UUID,
    ) -> t.Dict[str, int]:
        get_property = await super().get(property_id)
        if get_property is None:
            raise error.NotFoundError("Product not found")
        if get_property.hard_back_qty != 0 and get_property.hard_back_qty >= hard_back_qty:
            get_property.hard_back_qty = get_property.hard_back_qty - hard_back_qty
        if get_property.paper_back_qty != 0 and get_property.paper_back_qty >= paper_back_qty:
            get_property.paper_back_qty = get_property.paper_back_qty - paper_back_qty

        self.db.add(get_property)
        await self.db.commit()
        await self.db.refresh(get_property)
        return get_property


class ProductMediaRepository(BaseRepository[model.ProductMedia]):
    def __init__(self):
        super().__init__(model.ProductMedia)

    async def create_or_update(
        self,
        product_id: t.Optional[UUID] = None,
        gallery: t.Optional[t.List[UUID]] = [],
        pdf: t.Optional[UUID] = None,
        cover_img: t.Optional[UUID] = None,
    ) -> model.ProductMedia:
        if not gallery and not pdf and not cover_img:
            return None
        if product_id:
            check_media = await self.get_by_attr(
                attr=dict(product_id=product_id), first=True, load_related=True
            )
            if check_media and gallery:
                if gallery:
                    check_media.gallery.extend(gallery)
            if pdf and check_media:
                check_media.pdf = pdf
            if cover_img and check_media:
                check_media.cover_img = cover_img
            self.db.add(check_media)
            await self.db.commit()
            await self.db.refresh(check_media)
            self.db.expunge_all()
            return check_media
        new_product_media = dict()
        if gallery:
            new_product_media["gallery"] = gallery
        if pdf:
            new_product_media["pdf"] = pdf
        if cover_img:
            new_product_media["cover_img"] = cover_img
        if new_product_media.values() is not None:
            new_data = self.model(**new_product_media)
            self.db.add(new_data)
            await self.db.commit()
            self.db.expunge_all()
            return new_data
        return None

    async def delete(self, old_media: model.ProductMedia) -> bool:
        return await super().delete(old_media.id)


class ProductVariationRepository(BaseRepository[model.Product,]):
    def __init__(self):
        super().__init__(model.Product)

    async def add_variation(self, product: model.Product, variation: model.Product):
        if product:
            product.variations.extends(variation)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return True

    async def get_variation(self, variation_id: UUID):
        get_variation: model.Product = await super().get_by_attr(
            attr=dict(id=variation_id, is_series=False),
            first=True,
            load_related=True,
        )

        if not get_variation:
            raise error.NotFoundError(f"Variation with id {variation_id} does not exists")
        return get_variation

    async def remove_variation(self, obj: schema.IVariationProductIn):
        variation_to_update = await self.update(
            id=obj.variation_id,
            obj=dict(parent_id=None, is_series=False, is_assigned=False),
        )
        if variation_to_update:
            return variation_to_update
        return None


class ProductRepository(BaseRepository[model.Product]):
    def __init__(self):
        super().__init__(model.Product)

    async def create_product(
        self,
        obj: schema.IProductIn,
        categories: t.Optional[t.List[Category]] = None,
        properties: t.Optional[model.ProductProperty] = None,
        attributes: t.Optional[model.ProductAttribute] = None,
        medias: t.Optional[model.ProductMedia] = None,
    ) -> model.Product:
        to_create = dict()

        for key, val in obj.dict(exclude={"attribute", "property", "category", "medias"}).items():
            if hasattr(self.model, key):
                to_create[key] = val
        to_create["slug"] = self.make_slug(obj.name)
        if attributes:
            to_create["attribute"] = attributes
        if properties:
            to_create["property"] = properties
        if categories:
            to_create["categories"] = categories
        if medias:
            to_create["medias"] = medias

        new_product = self.model(**to_create)
        self.db.add(new_product)
        await self.db.commit()
        self.db.expunge_all()
        return new_product

    async def delete(self, product_id: UUID):
        return await super().delete(product_id)

    async def update_product(
        self,
        product: model.Product,
        obj: t.Union[schema.IProductIn, dict],
        categories: t.Optional[t.List[Category]] = [],
        medias: t.Optional[model.ProductMedia] = None,
    ):
        if isinstance(obj, BaseModel):
            for key, val in obj.dict(
                exclude={"attribute", "property", "category", "medias"}
            ).items():
                if hasattr(product, key):
                    if getattr(product, key) != val:
                        setattr(product, key, val)
        if isinstance(obj, dict):
            for key, val in obj.items():
                if hasattr(product, key):
                    if getattr(product, key) != val:
                        setattr(product, key, val)
        if medias:
            product.medias = medias
        if categories:
            product.categories.extends(categories)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        self.db.expunge_all()
        return product


product_repo = ProductRepository()
product_attribute_repo = ProductAttributeRepository()
product_property_repo = ProductPropertyRepository()
variation_repo = ProductVariationRepository()
product_media_repo = ProductMediaRepository()
