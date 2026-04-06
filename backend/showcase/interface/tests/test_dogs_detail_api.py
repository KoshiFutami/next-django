from datetime import date, datetime, timezone
from uuid import UUID, uuid4

import pytest
from django.test import Client
from django.test.utils import override_settings

from showcase.interface.tests.pii_test_util import (
    create_owner_profile,
    create_user,
)
from showcase.models import Breed as BreedRow
from showcase.models import Dog as DogRow

STUB_OWNER_ID = UUID("00000000-0000-0000-0000-000000000001")


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_detail_get_returns_dog():
    u = create_user("detail@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="detail@example.com",
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
    u_stub = create_user("stub2@example.com", "x")
    u_other = create_user("other2@example.com", "x")
    create_owner_profile(
        user=u_stub,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="stub2@example.com",
    )
    other_id = uuid4()
    create_owner_profile(
        user=u_other,
        owner_id=other_id,
        nickname="他人",
        account_email="other2@example.com",
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
    u = create_user("none@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="none@example.com",
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)

    client = Client()
    res = client.get(f"/api/dogs/{uuid4()}/")
    assert res.status_code == 404
    assert res.json()["code"] == "not_found"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_detail_post_method_not_allowed():
    u = create_user("mna@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="mna@example.com",
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
    u = create_user("del@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="del@example.com",
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
    u = create_user("del404@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="del404@example.com",
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)

    client = Client()
    res = client.delete(f"/api/dogs/{uuid4()}/")
    assert res.status_code == 404
    assert res.json()["code"] == "not_found"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_detail_delete_other_owners_dog_returns_404():
    u_stub = create_user("dstub@example.com", "x")
    u_other = create_user("dother@example.com", "x")
    create_owner_profile(
        user=u_stub,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="dstub@example.com",
    )
    other_id = uuid4()
    create_owner_profile(
        user=u_other,
        owner_id=other_id,
        nickname="他人",
        account_email="dother@example.com",
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
