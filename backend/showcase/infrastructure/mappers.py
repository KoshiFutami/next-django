"""ORM とドメインエンティティの相互変換。"""

from django.contrib.auth import get_user_model

from showcase.domain.breed import Breed
from showcase.domain.dog import Dog
from showcase.domain.email import Email
from showcase.domain.owner import Owner
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey
from showcase.models import Breed as BreedRow
from showcase.models import Dog as DogRow
from showcase.models import OwnerProfile as OwnerProfileRow


def owner_profile_to_domain(row: OwnerProfileRow) -> Owner:
    return Owner(
        id=OwnerId(value=row.id),
        email=Email.parse(row.user.email),
        nickname=row.nickname,
        profile_image_key=ProfileImageKey.parse(row.profile_image_key)
        if row.profile_image_key
        else None,
        created_at=row.created_at,
    )


def breed_row_to_domain(row: BreedRow) -> Breed:
    return Breed(code=row.code, name=row.name, sort_order=row.sort_order)


def dog_row_to_domain(row: DogRow) -> Dog:
    return Dog(
        id=row.id,
        name=row.name,
        birth_date=row.birth_date,
        weight=row.weight,
        color=row.color,
        gender=row.gender,
        owner_id=OwnerId(value=row.owner_id),
        breed_code=row.breed.code,
        profile_image_key=ProfileImageKey.parse(row.profile_image_key)
        if row.profile_image_key
        else None,
        created_at=row.created_at,
    )


def create_owner_with_password(owner: Owner, password: str) -> None:
    """新規 User + OwnerProfile を作成する。`username` はメールと同一。"""
    User = get_user_model()
    email = owner.email.value
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
    )
    OwnerProfileRow.objects.create(
        id=owner.id.value,
        user=user,
        nickname=owner.nickname,
        profile_image_key=owner.profile_image_key.value
        if owner.profile_image_key
        else None,
        created_at=owner.created_at,
    )


def persist_owner(owner: Owner) -> None:
    User = get_user_model()
    email = owner.email.value
    user, _ = User.objects.update_or_create(
        username=email,
        defaults={"email": email},
    )
    if not user.has_usable_password():
        user.set_unusable_password()
        user.save(update_fields=["password"])
    OwnerProfileRow.objects.update_or_create(
        id=owner.id.value,
        defaults={
            "user": user,
            "nickname": owner.nickname,
            "profile_image_key": owner.profile_image_key.value
            if owner.profile_image_key
            else None,
            "created_at": owner.created_at,
        },
    )


def persist_breed(breed: Breed) -> None:
    BreedRow.objects.update_or_create(
        code=breed.code,
        defaults={
            "name": breed.name,
            "sort_order": breed.sort_order,
        },
    )


def persist_dog(dog: Dog) -> None:
    owner_row = OwnerProfileRow.objects.get(pk=dog.owner_id.value)
    DogRow.objects.update_or_create(
        id=dog.id,
        defaults={
            "owner": owner_row,
            "breed_id": dog.breed_code,
            "name": dog.name,
            "birth_date": dog.birth_date,
            "weight": dog.weight,
            "color": dog.color,
            "gender": dog.gender,
            "profile_image_key": dog.profile_image_key.value
            if dog.profile_image_key
            else None,
            "created_at": dog.created_at,
        },
    )
