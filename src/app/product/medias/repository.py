from src._base.repository.base import BaseRepository
from src.app.product.medias import model


class ProductMediaRepository(BaseRepository[model.ProductMedia]):
    def __init__(self):
        super().__init__(model.ProductMedia)


product_media_repo = ProductMediaRepository()
