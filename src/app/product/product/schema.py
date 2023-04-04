import datetime
import typing as t
import uuid
import pydantic as pyd
from src.app.media_store import schema as media_schema


class IProductProperty(pyd.BaseModel):
    in_stock: bool
    has_pdf: bool = True
    discount: float = pyd.Field(gt=0, le=1)
    paper_back_price: t.Optional[pyd.condecimal(max_digits=10, decimal_places=2)]
    paper_back_qty: int = 10
    hard_back_price: t.Optional[pyd.condecimal(max_digits=10, decimal_places=2)]
    hard_back_qty: int = 10
    pdf_price: t.Optional[pyd.condecimal(max_digits=10, decimal_places=2)]


class IProductAttribute(pyd.BaseModel):
    isbn10: str
    isbn13: str
    height: float
    width: float
    weight: float
    pub_date: t.Optional[datetime.date] = datetime.datetime.today()


class IProductMediaIn(pyd.BaseModel):
    pdf: t.Optional[uuid.UUID] = None
    cover_img: t.Optional[uuid.UUID] = None
    gallery: t.Optional[t.List[uuid.UUID]] = None


class IProductMediaOut(pyd.BaseModel):
    cover_img: t.Optional[media_schema.IMedia]
    pdf: t.Optional[media_schema.IMedia]
    gallery: t.Optional[t.List[media_schema.IMedia]] = []


class IProductIn(pyd.BaseModel):
    name: str
    description: str
    amazon_link: t.Optional[pyd.HttpUrl] = None
    epub_link: t.Optional[pyd.HttpUrl] = None
    kindle_link: t.Optional[pyd.HttpUrl] = None
    is_series: bool = False
    is_active: bool = True
    category: t.List[t.Optional[str]] = []
    attribute: IProductAttribute
    property: IProductProperty
    medias: IProductMediaIn


class IProductShortInfo(pyd.BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: str
    slug: str
    is_series: bool
    amazon_link: t.Optional[str] = None
    epub_link: t.Optional[str] = None
    kindle_link: t.Optional[str] = None
    is_assigned: bool
    is_active: bool
    medias: IProductMediaOut

    class Config:
        orm_mode = True


class IProductLongInfo(IProductShortInfo):
    id: uuid.UUID
    attributes: IProductAttribute
    property: IProductProperty

    class Config:
        orm_mode = True


class IVariationProductIn(pyd.BaseModel):
    product_id: uuid.UUID
    variation_id: uuid.UUID
