from showcase.domain.dog import Dog
from showcase.domain.owner_id import OwnerId
from showcase.domain.repositories import DogRepository


class ListMyDogsUseCase:
    def __init__(self, dog_repository: DogRepository):
        self.dog_repository = dog_repository

    def execute(self, owner_id: OwnerId) -> list[Dog]:
        return self.dog_repository.list_by_owner(owner_id)
