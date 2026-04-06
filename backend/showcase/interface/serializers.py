"""HTTP レスポンス用: ドメイン → JSON 互換 dict。"""

from showcase.domain.breed import Breed
from showcase.domain.dog import Dog
from showcase.domain.owner import Owner


def refresh_access_to_json(*, access: str) -> dict:
    return {
        "access": access,
        "token_type": "Bearer",
    }


def login_result_to_json(*, access: str, refresh: str, owner: Owner) -> dict:
    return {
        "access": access,
        "refresh": refresh,
        "token_type": "Bearer",
        "owner": owner_to_json(owner),
    }


def owner_to_json(owner: Owner) -> dict:
    return {
        "id": str(owner.id.value),
        "email": owner.email.value,
        "nickname": owner.nickname,
        "full_name": owner.full_name,
        "handle": owner.handle,
        "profile_image_key": owner.profile_image_key.value
        if owner.profile_image_key
        else None,
        "created_at": owner.created_at.isoformat(),
    }


def dog_to_json(dog: Dog) -> dict:
    return {
        "id": str(dog.id),
        "name": dog.name,
        "birth_date": dog.birth_date.isoformat(),
        "weight": dog.weight,
        "color": dog.color,
        "gender": dog.gender,
        "breed_code": dog.breed_code,
        "profile_image_key": dog.profile_image_key.value
        if dog.profile_image_key
        else None,
        "created_at": dog.created_at.isoformat(),
    }


def breed_to_json(breed: Breed) -> dict:
    return {
        "code": breed.code,
        "name": breed.name,
        "sort_order": breed.sort_order,
    }
