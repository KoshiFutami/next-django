import json

import pytest
from django.test import Client

from showcase.models import Breed as BreedRow
from showcase.models import Dog as DogRow


@pytest.mark.django_db
def test_dogs_post_with_bearer_token_uses_registered_owner():
    client = Client()
    password = "dog_jwt_pass_9"
    reg = client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "dogowner_jwt@example.com",
                "password": password,
                "nickname": "JWT飼い主",
            }
        ),
        content_type="application/json",
    )
    assert reg.status_code == 201
    owner_id = reg.json()["id"]

    login = client.post(
        "/api/auth/login/",
        data=json.dumps({"email": "dogowner_jwt@example.com", "password": password}),
        content_type="application/json",
    )
    assert login.status_code == 200
    access = login.json()["access"]

    BreedRow.objects.create(code=99, name="テスト種", sort_order=1)

    res = client.post(
        "/api/dogs/",
        data=json.dumps(
            {
                "name": "JWT犬",
                "birth_date": "2022-01-01",
                "weight": 5.0,
                "color": "白",
                "gender": "male",
                "breed_code": 99,
            }
        ),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {access}",
    )
    assert res.status_code == 201
    dog = DogRow.objects.get(name="JWT犬")
    assert str(dog.owner_id) == owner_id


@pytest.mark.django_db
def test_dogs_post_with_invalid_bearer_returns_401():
    client = Client()
    BreedRow.objects.create(code=88, name="種", sort_order=1)
    res = client.post(
        "/api/dogs/",
        data=json.dumps(
            {
                "name": "失敗犬",
                "birth_date": "2022-01-01",
                "weight": 5.0,
                "color": "白",
                "gender": "male",
                "breed_code": 88,
            }
        ),
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer invalid.token.here",
    )
    assert res.status_code == 401
    assert res.json()["code"] == "unauthorized"
