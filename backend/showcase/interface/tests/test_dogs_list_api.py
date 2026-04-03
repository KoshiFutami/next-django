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
def test_dogs_list_returns_all_dogs_without_owner_filter():
    u_stub = create_user("stub@example.com", "x")
    u_other = create_user("other@example.com", "x")

    create_owner_profile(
        user=u_stub,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="stub@example.com",
    )
    other_id = uuid4()
    create_owner_profile(
        user=u_other,
        owner_id=other_id,
        nickname="他人",
        account_email="other@example.com",
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
    res = client.get("/api/dogs/")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 2
    ids = {item["id"] for item in data["items"]}
    assert ids == {str(mine.id), str(other_dog.id)}
    names = {item["name"] for item in data["items"]}
    assert names == {"ポチ", "他人の犬"}


@pytest.mark.django_db
def test_dogs_list_empty_when_no_dogs():
    u = create_user("empty@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="犬なし",
        account_email="empty@example.com",
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)

    client = Client()
    res = client.get("/api/dogs/")
    assert res.status_code == 200
    assert res.json() == {"items": []}
