import json

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from showcase.interface.tests.pii_test_util import login_username
from showcase.models import OwnerProfile as OwnerProfileRow


@pytest.mark.django_db
def test_auth_login_post_returns_tokens_and_owner():
    client = Client()
    password = "login_ok_pass_9"
    reg = client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "loginuser@example.com",
                "password": password,
                "nickname": "ログイン太郎",
                "full_name": "ログイン太郎本名",
                "handle": "login_user_h",
            }
        ),
        content_type="application/json",
    )
    assert reg.status_code == 201

    res = client.post(
        "/api/auth/login/",
        data=json.dumps({"email": "loginuser@example.com", "password": password}),
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.json()
    assert data["token_type"] == "Bearer"
    assert "access" in data and len(data["access"]) > 20
    assert "refresh" in data and len(data["refresh"]) > 20
    assert data["owner"]["email"] == "loginuser@example.com"
    assert data["owner"]["nickname"] == "ログイン太郎"


@pytest.mark.django_db
def test_auth_login_wrong_password_returns_401():
    client = Client()
    password = "right_pass_9"
    client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "wrongpw@example.com",
                "password": password,
                "nickname": "ユーザー",
                "full_name": "ユーザー本名",
                "handle": "wrongpw_h",
            }
        ),
        content_type="application/json",
    )
    res = client.post(
        "/api/auth/login/",
        data=json.dumps({"email": "wrongpw@example.com", "password": "wrong_pass_9"}),
        content_type="application/json",
    )
    assert res.status_code == 401
    assert res.json()["code"] == "invalid_credentials"


@pytest.mark.django_db
def test_auth_login_unknown_email_returns_401():
    client = Client()
    res = client.post(
        "/api/auth/login/",
        data=json.dumps({"email": "nobody@example.com", "password": "any_pass_9"}),
        content_type="application/json",
    )
    assert res.status_code == 401
    assert res.json()["code"] == "invalid_credentials"


@pytest.mark.django_db
def test_auth_login_missing_password_returns_400():
    client = Client()
    res = client.post(
        "/api/auth/login/",
        data=json.dumps({"email": "a@example.com"}),
        content_type="application/json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_auth_login_user_without_profile_returns_401():
    User = get_user_model()
    User.objects.create_user(
        username=login_username("orphan@example.com"),
        email="",
        password="orphan_pass_9",
    )
    assert not OwnerProfileRow.objects.filter(
        user__username="orphan@example.com"
    ).exists()
    client = Client()
    res = client.post(
        "/api/auth/login/",
        data=json.dumps(
            {
                "email": "orphan@example.com",
                "password": "orphan_pass_9",
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 401
    assert res.json()["code"] == "invalid_credentials"


@pytest.mark.django_db
def test_auth_login_get_returns_405():
    client = Client()
    res = client.get("/api/auth/login/")
    assert res.status_code == 405
