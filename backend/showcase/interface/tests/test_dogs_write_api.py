import json
from datetime import datetime, timezone
from uuid import UUID

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.test.utils import override_settings

from showcase.models import Breed as BreedRow
from showcase.models import Dog as DogRow
from showcase.models import OwnerProfile as OwnerProfileRow

STUB_OWNER_ID = UUID("00000000-0000-0000-0000-000000000001")


def _stub_owner_and_breed():
    User = get_user_model()
    u = User.objects.create_user(username="stub-w@example.com", email="stub-w@example.com", password="x")
    OwnerProfileRow.objects.create(
        id=STUB_OWNER_ID,
        user=u,
        nickname="スタブ",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    BreedRow.objects.create(code=1, name="柴犬", sort_order=10)


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_post_json_creates_dog():
    _stub_owner_and_breed()
    client = Client()
    body = {
        "name": "ポチ",
        "birth_date": "2021-05-01",
        "weight": 8.0,
        "color": "茶",
        "gender": "male",
        "breed_code": 1,
    }
    res = client.post(
        "/api/dogs/",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "ポチ"
    assert data["breed_code"] == 1
    assert DogRow.objects.filter(owner_id=STUB_OWNER_ID, name="ポチ").exists()


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_delete_method_not_allowed():
    _stub_owner_and_breed()
    client = Client()
    res = client.delete("/api/dogs/")
    assert res.status_code == 405
    assert res.json()["code"] == "method_not_allowed"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_dogs_post_invalid_birth_date_returns_400():
    _stub_owner_and_breed()
    client = Client()
    body = {
        "name": "ポチ",
        "birth_date": "not-a-date",
        "weight": 8.0,
        "color": "茶",
        "gender": "male",
        "breed_code": 1,
    }
    res = client.post(
        "/api/dogs/",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert res.status_code == 400
    assert res.json()["code"] == "bad_request"
