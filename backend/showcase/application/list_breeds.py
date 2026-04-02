from showcase.domain.breed import Breed
from showcase.domain.repositories import BreedRepository


class ListBreedsUseCase:
    def __init__(self, breed_repository: BreedRepository):
        self.breed_repository = breed_repository

    def execute(self) -> list[Breed]:
        return self.breed_repository.list_ordered()
