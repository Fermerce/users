from core.repository.base import BaseRepository
from src.app.market.delivery_model import model


class DeliveryModeRepository(BaseRepository[model.OrderDeliveryMode,]):
    def __init__(self):
        super().__init__(model.OrderDeliveryMode)


delivery_mode_repo = DeliveryModeRepository()
