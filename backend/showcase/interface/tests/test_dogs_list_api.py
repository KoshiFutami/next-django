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
def test_dogs_list_returns_only_stub_owner_dogs():
    User = get_user_model()
    u_stub = User.objects.create_user(username="stub@example.com", email="stub@example.com", password="x")
    u_other = User.objects.create_user(username="other@example.com", email="other@example.com", password="x")

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

    mine = DogRow.objects.create(
        owner_id=STUB_OWNER_ID,
        breed_id=1,
        name="ポチ",
        birth_date=date(2021, 5, 1),
        weight=8.0,
        color="茶",
        gender="male",
        created_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )
    DogRow.objects.create(
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
    res = client.get("/api/dogs/")
    assert res.status_code == 200
    data = res.json()
    assert data["items"]
    assert len(data["items"]) == 1
    item = data["items"][0]
    assert item["id"] == str(mine.id)
    assert item["name"] == "ポチ"
    assert item["breed_code"] == 1


@pytest.mark.django_db
def test_dogs_list_empty_when_no_dogs():
    User = get_user_model()
    u = User.objects.create_user(username="empty@example.com", email="empty@example.com", password="x")
    OwnerProfileRow.objects.create(
        id=STUB_OWNER_ID,
        user=u,
        nickname="犬なし",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)

    client = Client()
    with override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID)):
        res = client.get("/api/dogs/")
    assert res.status_code == 200
    assert res.json() == {"items": []}
