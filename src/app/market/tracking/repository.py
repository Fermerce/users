from core.repository.base import BaseRepository
from src.app.market.tracking import model


class Tracking(BaseRepository[model.Tracking]):
    def __init__(self):
        super().__init__(model.Tracking)


tracking_repo = Tracking()
