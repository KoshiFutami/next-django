from datetime import date, datetime, timezone
from uuid import uuid4

import pytest

from showcase.domain.dog import Dog
from showcase.domain.exceptions import DomainValidationError
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey


def test_dog_construct_without_profile_image():
    owner_id = OwnerId.generate()
    dog_id = uuid4()
    dog = Dog(
        id=dog_id,
        name="ぽち",
        birth_date=date(2020, 3, 15),
        weight=5.5,
        color="茶",
        gender="male",
        owner_id=owner_id,
        breed_code=101,
    )
    assert dog.id == dog_id
    assert dog.name == "ぽち"
    assert dog.birth_date == date(2020, 3, 15)
    assert dog.weight == 5.5
    assert dog.color == "茶"
    assert dog.gender == "male"
    assert dog.owner_id == owner_id
    assert dog.breed_code == 101
    assert dog.profile_image_key is None


def test_dog_construct_with_profile_image():
    owner_id = OwnerId.generate()
    key = ProfileImageKey.parse("uploads/dogs/xyz.webp")
    dog = Dog(
        id=uuid4(),
        name="ハナ",
        birth_date=date(2019, 1, 1),
        weight=3.0,
        color="白",
        gender="female",
        owner_id=owner_id,
        breed_code=42,
        profile_image_key=key,
    )
    assert dog.profile_image_key == key


def test_dog_merge_patch_updates_single_field():
    owner_id = OwnerId.generate()
    created_at = datetime(2024, 6, 1, tzinfo=timezone.utc)
    dog = Dog(
        id=uuid4(),
        name="ぽち",
        birth_date=date(2020, 3, 15),
        weight=5.5,
        color="茶",
        gender="male",
        owner_id=owner_id,
        breed_code=101,
        created_at=created_at,
    )
    updated = dog.merge_patch({"name": "タロウ"})
    assert updated.name == "タロウ"
    assert updated.birth_date == dog.birth_date
    assert updated.id == dog.id
    assert updated.created_at == dog.created_at


def test_dog_merge_patch_invalid_weight_raises():
    owner_id = OwnerId.generate()
    dog = Dog(
        id=uuid4(),
        name="ぽち",
        birth_date=date(2020, 3, 15),
        weight=5.5,
        color="茶",
        gender="male",
        owner_id=owner_id,
        breed_code=101,
    )
    with pytest.raises(DomainValidationError):
        dog.merge_patch({"weight": 0})
