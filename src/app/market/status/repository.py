from core.repository.base import BaseRepository
from src.app.market.status import model


class StatusRepository(BaseRepository[model.Status]):
    def __init__(self):
        super().__init__(model.Status)


status_repo = StatusRepository()
