"""HTTP レスポンス用: ドメイン → JSON 互換 dict。"""

from showcase.domain.breed import Breed
from showcase.domain.dog import Dog


def dog_to_json(dog: Dog) -> dict:
    return {
        "id": str(dog.id),
        "name": dog.name,
        "birth_date": dog.birth_date.isoformat(),
        "weight": dog.weight,
        "color": dog.color,
        "gender": dog.gender,
        "breed_code": dog.breed_code,
        "profile_image_key": dog.profile_image_key.value if dog.profile_image_key else None,
        "created_at": dog.created_at.isoformat(),
    }

def breed_to_json(breed: Breed) -> dict:
    return {
        "code": breed.code,
        "name": breed.name,
        "sort_order": breed.sort_order,
    }
