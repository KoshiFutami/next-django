import json
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
def test_dogs_patch_updates_name():
    u = create_user("patch@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="patch@example.com",
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
    res = client.patch(
        f"/api/dogs/{dog.id}/",
        data=json.dumps({"name": "タロウ"}),
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.json()["name"] == "タロウ"
    assert res.json()["breed_code"] == 1
    dog.refresh_from_db()
    assert dog.name == "タロウ"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_patch_unknown_dog_returns_404():
    u = create_user("p404@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="p404@example.com",
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=0)

    client = Client()
    res = client.patch(
        f"/api/dogs/{uuid4()}/",
        data=json.dumps({"name": "x"}),
        content_type="application/json",
    )
    assert res.status_code == 404
    assert res.json()["code"] == "not_found"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_patch_invalid_birth_date_returns_400():
    u = create_user("p400@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="p400@example.com",
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
    res = client.patch(
        f"/api/dogs/{dog.id}/",
        data=json.dumps({"birth_date": "not-a-date"}),
        content_type="application/json",
    )
    assert res.status_code == 400
    assert res.json()["code"] == "bad_request"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_patch_ignores_unknown_json_keys():
    u = create_user("pign@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="pign@example.com",
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
    res = client.patch(
        f"/api/dogs/{dog.id}/",
        data=json.dumps({"name": "新名", "owner_id": str(uuid4())}),
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.json()["name"] == "新名"
    dog.refresh_from_db()
    assert dog.owner_id == STUB_OWNER_ID
    assert dog.name == "新名"
