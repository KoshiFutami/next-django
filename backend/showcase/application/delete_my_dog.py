from uuid import UUID

from showcase.domain.owner_id import OwnerId
from showcase.domain.repositories import DogRepository


class DeleteMyDogUseCase:
    def __init__(self, dog_repository: DogRepository):
        self.dog_repository = dog_repository

    def execute(self, owner_id: OwnerId, dog_id: UUID) -> int:
        """指定オーナーに紐づく犬を削除する。削除した `Dog` 行数（対象なしは 0）。"""
        return self.dog_repository.delete_by_id_for_owner(owner_id, dog_id)
