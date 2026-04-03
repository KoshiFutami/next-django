from showcase.domain.dog import Dog
from showcase.domain.repositories import DogRepository


class ListAllDogsUseCase:
    def __init__(self, dog_repository: DogRepository):
        self.dog_repository = dog_repository

    def execute(self) -> list[Dog]:
        """登録済みの犬を一覧する（オーナー制限なし・閲覧用）。"""
        return self.dog_repository.list_all_ordered()
