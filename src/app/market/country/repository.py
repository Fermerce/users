from core.repository.base import BaseRepository
from src.app.market.country import model


class CountryRepository(BaseRepository[model.Country,]):
    def __init__(self):
        super().__init__(model.Country)


country_repo = CountryRepository()
