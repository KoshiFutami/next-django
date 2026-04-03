from datetime import date
from uuid import uuid4

import pytest

from showcase.domain.breed import Breed
from showcase.domain.dog import Dog
from showcase.domain.email import Email
from showcase.domain.owner import Owner
from showcase.domain.profile_image_key import ProfileImageKey
from showcase.infrastructure.django_repositories import (
    DjangoBreedRepository,
    DjangoDogRepository,
    DjangoOwnerRepository,
)


@pytest.mark.django_db
def test_owner_roundtrip():
    owner = Owner.register(email=Email.parse("a@example.com"), nickname="太郎")
    repos = DjangoOwnerRepository()
    repos.save(owner)
    got = repos.get_by_id(owner.id)
    assert got is not None
    assert got.id == owner.id
    assert got.nickname == "太郎"
    assert got.email.value == "a@example.com"

    by_email = repos.get_by_email(Email.parse("a@example.com"))
    assert by_email is not None
    assert by_email.id == owner.id


@pytest.mark.django_db
def test_breed_and_dog_roundtrip():
    breed = Breed.create(code=1, name="柴犬", sort_order=0)
    breed_repos = DjangoBreedRepository()
    breed_repos.save(breed)

    owner = Owner.register(email=Email.parse("dogowner@example.com"), nickname="花子")
    DjangoOwnerRepository().save(owner)

    dog = Dog(
        id=uuid4(),
        name="ポチ",
        birth_date=date(2021, 5, 1),
        weight=8.0,
        color="茶",
        gender="male",
        owner_id=owner.id,
        breed_code=1,
        profile_image_key=ProfileImageKey.parse("uploads/dogs/p.webp"),
    )
    dog_repos = DjangoDogRepository()
    dog_repos.save(dog)

    got = dog_repos.get_by_id(dog.id)
    assert got is not None
    assert got.name == "ポチ"
    assert got.breed_code == 1
    assert got.profile_image_key is not None

    listed = dog_repos.list_by_owner(owner.id)
    assert len(listed) == 1
    assert listed[0].id == dog.id
