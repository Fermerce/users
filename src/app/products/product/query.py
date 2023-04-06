import typing as t
from uuid import UUID
from pydantic import BaseModel
from src.app.products.category.model import ProductCategory
from core.query.base_query import BaseQuery
from src.app.products import model, schema


class ProductQuery(BaseQuery[model.Product]):
    def __init__(self):
        super().__init__(model.Product)

    async def create_product(
        self,
        obj: schema.IProductIn,
        categories: t.Optional[t.List[ProductCategory]] = None,
        properties: t.Optional[model.ProductProperty] = None,
        attributes: t.Optional[model.ProductAttribute] = None,
        medias: t.Optional[model.ProductMedia] = None,
    ) -> model.Product:
        to_create = dict()

        for key, val in obj.dict(
            exclude={"attribute", "property", "category", "medias"}
        ).items():
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
        categories: t.Optional[t.List[ProductCategory]] = [],
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


product_query = ProductQuery()
