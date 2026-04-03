from datetime import date
from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model

from showcase.domain.breed import Breed
from showcase.domain.dog import Dog
from showcase.domain.email import Email
from showcase.domain.exceptions import EmailAlreadyRegisteredError
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
def test_register_with_password_roundtrip():
    owner = Owner.register(email=Email.parse("reg@example.com"), nickname="登録")
    repos = DjangoOwnerRepository()
    assert repos.is_email_registered(Email.parse("reg@example.com")) is False
    repos.register_with_password(owner, "repo_test_pass_9")
    assert repos.is_email_registered(Email.parse("reg@example.com")) is True
    got = repos.get_by_email(Email.parse("reg@example.com"))
    assert got is not None
    assert got.nickname == "登録"
    u = get_user_model().objects.get(username="reg@example.com")
    assert u.check_password("repo_test_pass_9")


@pytest.mark.django_db
def test_register_with_password_duplicate_raises():
    owner = Owner.register(email=Email.parse("twice@example.com"), nickname="A")
    repos = DjangoOwnerRepository()
    repos.register_with_password(owner, "dup_test_pass_9")
    other = Owner.register(email=Email.parse("twice@example.com"), nickname="B")
    with pytest.raises(EmailAlreadyRegisteredError):
        repos.register_with_password(other, "dup_test_pass_9b")


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

    by_owner = dog_repos.get_by_id_for_owner(owner.id, dog.id)
    assert by_owner is not None
    assert by_owner.id == dog.id


@pytest.mark.django_db
def test_dog_get_by_id_for_owner_wrong_owner_returns_none():
    breed = Breed.create(code=1, name="柴犬", sort_order=0)
    DjangoBreedRepository().save(breed)

    owner_a = Owner.register(email=Email.parse("a@example.com"), nickname="A")
    owner_b = Owner.register(email=Email.parse("b@example.com"), nickname="B")
    DjangoOwnerRepository().save(owner_a)
    DjangoOwnerRepository().save(owner_b)

    dog = Dog(
        id=uuid4(),
        name="共有しない犬",
        birth_date=date(2021, 5, 1),
        weight=8.0,
        color="茶",
        gender="male",
        owner_id=owner_a.id,
        breed_code=1,
        profile_image_key=None,
    )
    dog_repos = DjangoDogRepository()
    dog_repos.save(dog)

    assert dog_repos.get_by_id_for_owner(owner_b.id, dog.id) is None
