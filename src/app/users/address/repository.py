from core.repository.base import BaseRepository
from src.app.users.address import model


class AddressRepository(BaseRepository[model.ShippingAddress]):
    def __init__(self):
        super().__init__(model.ShippingAddress)


address_repo = AddressRepository()
