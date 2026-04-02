from datetime import date
from uuid import uuid4

from showcase.domain.dog import Dog
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
