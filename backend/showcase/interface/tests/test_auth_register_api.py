import json

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from showcase.interface.tests.pii_test_util import login_username
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
    assert data["full_name"] == ""
    assert data["handle"] is None
    assert "id" in data
    user = get_user_model().objects.get(username=login_username("newuser@example.com"))
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
def test_auth_register_with_full_name_and_handle():
    client = Client()
    res = client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "named@example.com",
                "password": "named_register_pass_9",
                "nickname": "表示名",
                "full_name": "  本名 太郎  ",
                "handle": "@honmei_taro",
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 201
    data = res.json()
    assert data["full_name"] == "本名 太郎"
    assert data["handle"] == "honmei_taro"
    row = OwnerProfileRow.objects.get(pk=data["id"])
    assert row.full_name == "本名 太郎"
    assert row.handle == "honmei_taro"


@pytest.mark.django_db
def test_auth_register_duplicate_handle_returns_409():
    client = Client()
    body_base = {
        "password": "handle_dup_pass_9",
        "nickname": "u",
        "handle": "same_handle_9",
    }
    r1 = client.post(
        "/api/auth/register/",
        data=json.dumps({"email": "first@example.com", **body_base}),
        content_type="application/json",
    )
    assert r1.status_code == 201
    r2 = client.post(
        "/api/auth/register/",
        data=json.dumps({"email": "second@example.com", **body_base}),
        content_type="application/json",
    )
    assert r2.status_code == 409
    assert r2.json()["code"] == "handle_already_registered"


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
