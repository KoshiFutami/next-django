from datetime import date

from showcase.domain.dog import Dog
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey
from showcase.domain.repositories import DogRepository


class CreateMyDogUseCase:
    def __init__(self, dog_repository: DogRepository):
        """登録先のリポジトリを受け取る。"""
        self.dog_repository = dog_repository

    def execute(self, owner_id: OwnerId, post_params: dict) -> Dog:
        """入力値から Dog を生成して保存し、保存済みエンティティを返す。"""
        dog = Dog.register(
            name=post_params.get("name"),
            birth_date=date.fromisoformat(post_params.get("birth_date")),
            weight=float(post_params.get("weight")) or 0.0,
            color=post_params.get("color"),
            gender=post_params.get("gender"),
            owner_id=owner_id,
            breed_code=int(post_params.get("breed_code")) or 0,
            profile_image_key=ProfileImageKey.parse(
                post_params.get("profile_image_key")
            )
            if post_params.get("profile_image_key")
            else None,
        )
        self.dog_repository.save(dog)
        return dog
