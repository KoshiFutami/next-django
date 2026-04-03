from uuid import UUID

from showcase.domain.dog import Dog
from showcase.domain.owner_id import OwnerId
from showcase.domain.repositories import DogRepository


class GetMyDogUseCase:
    def __init__(self, dog_repository: DogRepository):
        self.dog_repository = dog_repository

    def execute(self, owner_id: OwnerId, dog_id: UUID) -> Dog | None:
        """指定オーナーに紐づく犬を 1 件取得する。該当なしは None。"""
        return self.dog_repository.get_by_id_for_owner(owner_id, dog_id)
