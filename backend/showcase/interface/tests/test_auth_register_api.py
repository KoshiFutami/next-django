import json

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from showcase.models import OwnerProfile as OwnerProfileRow


@pytest.mark.django_db
def test_auth_register_post_creates_owner_and_profile():
    client = Client()
    res = client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "  NewUser@Example.COM ",
                "password": "register_test_pass_9",
                "nickname": " 登録ユーザー ",
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "newuser@example.com"
    assert data["nickname"] == "登録ユーザー"
    assert "id" in data
    user = get_user_model().objects.get(username="newuser@example.com")
    assert user.check_password("register_test_pass_9")
    assert OwnerProfileRow.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_auth_register_duplicate_email_returns_409():
    client = Client()
    body = {
        "email": "dup@example.com",
        "password": "dup_register_pass_9",
        "nickname": "1人目",
    }
    r1 = client.post(
        "/api/auth/register/",
        data=json.dumps(body),
        content_type="application/json",
    )
    assert r1.status_code == 201
    r2 = client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "dup@example.com",
                "password": "another_pass_9",
                "nickname": "2人目",
            }
        ),
        content_type="application/json",
    )
    assert r2.status_code == 409
    assert r2.json()["code"] == "email_already_registered"


@pytest.mark.django_db
def test_auth_register_weak_password_returns_400():
    client = Client()
    res = client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "weak@example.com",
                "password": "12345",
                "nickname": "太郎",
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 400
    assert res.json()["code"] == "bad_request"


@pytest.mark.django_db
def test_auth_register_missing_email_returns_400():
    client = Client()
    res = client.post(
        "/api/auth/register/",
        data=json.dumps({"password": "ok_pass_9", "nickname": "太郎"}),
        content_type="application/json",
    )
    assert res.status_code == 400
    assert "email" in res.json()["message"]


@pytest.mark.django_db
def test_auth_register_invalid_email_returns_400():
    client = Client()
    res = client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "not-an-email",
                "password": "ok_pass_9",
                "nickname": "太郎",
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 400
    assert res.json()["code"] == "bad_request"


@pytest.mark.django_db
def test_auth_register_get_returns_405():
    client = Client()
    res = client.get("/api/auth/register/")
    assert res.status_code == 405
    assert res.json()["code"] == "method_not_allowed"
