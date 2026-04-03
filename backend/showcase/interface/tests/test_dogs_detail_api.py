from datetime import date, datetime, timezone
from uuid import UUID, uuid4

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.test.utils import override_settings

from showcase.models import Breed as BreedRow
from showcase.models import Dog as DogRow
from showcase.models import OwnerProfile as OwnerProfileRow

STUB_OWNER_ID = UUID("00000000-0000-0000-0000-000000000001")


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_detail_get_returns_dog():
    User = get_user_model()
    u = User.objects.create_user(
        username="detail@example.com", email="detail@example.com", password="x"
    )
    OwnerProfileRow.objects.create(
        id=STUB_OWNER_ID,
        user=u,
        nickname="スタブ",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)
    dog = DogRow.objects.create(
        owner_id=STUB_OWNER_ID,
        breed_id=1,
        name="ポチ",
        birth_date=date(2021, 5, 1),
        weight=8.0,
        color="茶",
        gender="male",
        created_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )

    client = Client()
    res = client.get(f"/api/dogs/{dog.id}/")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == str(dog.id)
    assert data["name"] == "ポチ"
    assert data["breed_code"] == 1


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_detail_get_other_owners_dog_returns_200():
    User = get_user_model()
    u_stub = User.objects.create_user(
        username="stub2@example.com", email="stub2@example.com", password="x"
    )
    u_other = User.objects.create_user(
        username="other2@example.com", email="other2@example.com", password="x"
    )
    OwnerProfileRow.objects.create(
        id=STUB_OWNER_ID,
        user=u_stub,
        nickname="スタブ",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    other_id = uuid4()
    OwnerProfileRow.objects.create(
        id=other_id,
        user=u_other,
        nickname="他人",
        created_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)
    other_dog = DogRow.objects.create(
        owner_id=other_id,
        breed_id=1,
        name="他人の犬",
        birth_date=date(2022, 1, 1),
        weight=5.0,
        color="白",
        gender="female",
        created_at=datetime(2024, 6, 2, tzinfo=timezone.utc),
    )

    client = Client()
    res = client.get(f"/api/dogs/{other_dog.id}/")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == str(other_dog.id)
    assert data["name"] == "他人の犬"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_detail_unknown_id_returns_404():
    User = get_user_model()
    u = User.objects.create_user(
        username="none@example.com", email="none@example.com", password="x"
    )
    OwnerProfileRow.objects.create(
        id=STUB_OWNER_ID,
        user=u,
        nickname="スタブ",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)

    client = Client()
    res = client.get(f"/api/dogs/{uuid4()}/")
    assert res.status_code == 404
    assert res.json()["code"] == "not_found"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_detail_post_method_not_allowed():
    User = get_user_model()
    u = User.objects.create_user(
        username="mna@example.com", email="mna@example.com", password="x"
    )
    OwnerProfileRow.objects.create(
        id=STUB_OWNER_ID,
        user=u,
        nickname="スタブ",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)
    dog = DogRow.objects.create(
        owner_id=STUB_OWNER_ID,
        breed_id=1,
        name="ポチ",
        birth_date=date(2021, 5, 1),
        weight=8.0,
        color="茶",
        gender="male",
        created_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )

    client = Client()
    res = client.post(f"/api/dogs/{dog.id}/", data={})
    assert res.status_code == 405
    assert res.json()["code"] == "method_not_allowed"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_detail_delete_returns_204_and_removes_row():
    User = get_user_model()
    u = User.objects.create_user(
        username="del@example.com", email="del@example.com", password="x"
    )
    OwnerProfileRow.objects.create(
        id=STUB_OWNER_ID,
        user=u,
        nickname="スタブ",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)
    dog = DogRow.objects.create(
        owner_id=STUB_OWNER_ID,
        breed_id=1,
        name="ポチ",
        birth_date=date(2021, 5, 1),
        weight=8.0,
        color="茶",
        gender="male",
        created_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )

    client = Client()
    res = client.delete(f"/api/dogs/{dog.id}/")
    assert res.status_code == 204
    assert res.content == b""
    assert not DogRow.objects.filter(pk=dog.id).exists()


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_detail_delete_unknown_returns_404():
    User = get_user_model()
    u = User.objects.create_user(
        username="del404@example.com", email="del404@example.com", password="x"
    )
    OwnerProfileRow.objects.create(
        id=STUB_OWNER_ID,
        user=u,
        nickname="スタブ",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)

    client = Client()
    res = client.delete(f"/api/dogs/{uuid4()}/")
    assert res.status_code == 404
    assert res.json()["code"] == "not_found"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_detail_delete_other_owners_dog_returns_404():
    User = get_user_model()
    u_stub = User.objects.create_user(
        username="dstub@example.com", email="dstub@example.com", password="x"
    )
    u_other = User.objects.create_user(
        username="dother@example.com", email="dother@example.com", password="x"
    )
    OwnerProfileRow.objects.create(
        id=STUB_OWNER_ID,
        user=u_stub,
        nickname="スタブ",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    other_id = uuid4()
    OwnerProfileRow.objects.create(
        id=other_id,
        user=u_other,
        nickname="他人",
        created_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)
    other_dog = DogRow.objects.create(
        owner_id=other_id,
        breed_id=1,
        name="他人の犬",
        birth_date=date(2022, 1, 1),
        weight=5.0,
        color="白",
        gender="female",
        created_at=datetime(2024, 6, 2, tzinfo=timezone.utc),
    )

    client = Client()
    res = client.delete(f"/api/dogs/{other_dog.id}/")
    assert res.status_code == 404
    assert res.json()["code"] == "not_found"
    assert DogRow.objects.filter(pk=other_dog.id).exists()
