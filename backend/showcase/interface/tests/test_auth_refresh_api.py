import json

import pytest
from django.test import Client


@pytest.mark.django_db
def test_auth_refresh_post_returns_new_access():
    client = Client()
    password = "refresh_flow_pass_9"
    client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "refreshflow@example.com",
                "password": password,
                "nickname": "更新ユーザー",
            }
        ),
        content_type="application/json",
    )
    login = client.post(
        "/api/auth/login/",
        data=json.dumps({"email": "refreshflow@example.com", "password": password}),
        content_type="application/json",
    )
    assert login.status_code == 200
    refresh = login.json()["refresh"]
    old_access = login.json()["access"]

    res = client.post(
        "/api/auth/refresh/",
        data=json.dumps({"refresh": refresh}),
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.json()
    assert data["token_type"] == "Bearer"
    assert "access" in data
    assert data["access"] != old_access

    me = client.get(
        "/api/auth/me/",
        HTTP_AUTHORIZATION=f"Bearer {data['access']}",
    )
    assert me.status_code == 200
    assert me.json()["email"] == "refreshflow@example.com"


@pytest.mark.django_db
def test_auth_refresh_invalid_token_returns_401():
    client = Client()
    res = client.post(
        "/api/auth/refresh/",
        data=json.dumps({"refresh": "not-a-valid-refresh-jwt"}),
        content_type="application/json",
    )
    assert res.status_code == 401
    assert res.json()["code"] == "invalid_refresh_token"


@pytest.mark.django_db
def test_auth_refresh_missing_refresh_returns_400():
    client = Client()
    res = client.post(
        "/api/auth/refresh/",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_auth_refresh_get_returns_405():
    client = Client()
    res = client.get("/api/auth/refresh/")
    assert res.status_code == 405
