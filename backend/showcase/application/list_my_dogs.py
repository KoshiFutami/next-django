from showcase.domain.dog import Dog
from showcase.domain.owner_id import OwnerId
from showcase.domain.repositories import DogRepository


class ListMyDogsUseCase:
    def __init__(self, dog_repository: DogRepository):
        """参照先のリポジトリを受け取る。"""
        self.dog_repository = dog_repository

    def execute(self, owner_id: OwnerId) -> list[Dog]:
        """指定オーナーに紐づく犬一覧を返す。"""
        return self.dog_repository.list_by_owner(owner_id)
