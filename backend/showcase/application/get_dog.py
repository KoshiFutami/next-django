from uuid import UUID

from showcase.domain.dog import Dog
from showcase.domain.repositories import DogRepository


class GetDogUseCase:
    def __init__(self, dog_repository: DogRepository):
        self.dog_repository = dog_repository

    def execute(self, dog_id: UUID) -> Dog | None:
        """ID で犬を取得する（オーナー制限なし・閲覧用）。"""
        return self.dog_repository.get_by_id(dog_id)
