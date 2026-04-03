import json

import pytest
from django.test import Client


@pytest.mark.django_db
def test_auth_logout_blacklists_refresh_so_refresh_endpoint_fails():
    client = Client()
    password = "logout_flow_pass_9"
    client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "logoutflow@example.com",
                "password": password,
                "nickname": "ログアウト太郎",
            }
        ),
        content_type="application/json",
    )
    login = client.post(
        "/api/auth/login/",
        data=json.dumps({"email": "logoutflow@example.com", "password": password}),
        content_type="application/json",
    )
    assert login.status_code == 200
    access = login.json()["access"]
    refresh = login.json()["refresh"]

    out = client.post(
        "/api/auth/logout/",
        data=json.dumps({"refresh": refresh}),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {access}",
    )
    assert out.status_code == 204
    assert out.content == b""

    again = client.post(
        "/api/auth/refresh/",
        data=json.dumps({"refresh": refresh}),
        content_type="application/json",
    )
    assert again.status_code == 401
    assert again.json()["code"] == "invalid_refresh_token"


@pytest.mark.django_db
def test_auth_logout_without_bearer_returns_401():
    client = Client()
    res = client.post(
        "/api/auth/logout/",
        data=json.dumps({"refresh": "x"}),
        content_type="application/json",
    )
    assert res.status_code == 401
    assert res.json()["code"] == "unauthorized"


@pytest.mark.django_db
def test_auth_logout_mismatched_refresh_returns_403():
    client = Client()
    pw_a = "logout_a_pass_9"
    pw_b = "logout_b_pass_9"
    client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "logout_a@example.com",
                "password": pw_a,
                "nickname": "A",
            }
        ),
        content_type="application/json",
    )
    client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "logout_b@example.com",
                "password": pw_b,
                "nickname": "B",
            }
        ),
        content_type="application/json",
    )
    login_a = client.post(
        "/api/auth/login/",
        data=json.dumps({"email": "logout_a@example.com", "password": pw_a}),
        content_type="application/json",
    )
    login_b = client.post(
        "/api/auth/login/",
        data=json.dumps({"email": "logout_b@example.com", "password": pw_b}),
        content_type="application/json",
    )
    access_a = login_a.json()["access"]
    refresh_b = login_b.json()["refresh"]

    res = client.post(
        "/api/auth/logout/",
        data=json.dumps({"refresh": refresh_b}),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {access_a}",
    )
    assert res.status_code == 403
    assert res.json()["code"] == "forbidden"


@pytest.mark.django_db
def test_auth_logout_missing_refresh_returns_400():
    client = Client()
    client.post(
        "/api/auth/register/",
        data=json.dumps(
            {
                "email": "missrefresh@example.com",
                "password": "miss_pass_9",
                "nickname": "M",
            }
        ),
        content_type="application/json",
    )
    login = client.post(
        "/api/auth/login/",
        data=json.dumps(
            {"email": "missrefresh@example.com", "password": "miss_pass_9"}
        ),
        content_type="application/json",
    )
    access = login.json()["access"]
    res = client.post(
        "/api/auth/logout/",
        data=json.dumps({}),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {access}",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_auth_logout_get_returns_405():
    client = Client()
    res = client.get("/api/auth/logout/")
    assert res.status_code == 405
