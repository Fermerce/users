from core.repository.base import BaseRepository
from src.app.market.state import model


class CountryRepository(BaseRepository[model.State]):
    def __init__(self):
        super().__init__(model.State)


state_repo = CountryRepository()
