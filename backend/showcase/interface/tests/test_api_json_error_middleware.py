import pytest
from django.test import Client
from django.test.utils import override_settings


@pytest.mark.django_db
@override_settings(DEBUG=True)
def test_api_unknown_path_returns_json_404_not_html():
    client = Client()
    res = client.get("/api/this-route-does-not-exist/")
    assert res.status_code == 404
    assert res["Content-Type"].startswith("application/json")
    data = res.json()
    assert data["code"] == "not_found"
    assert "message" in data


@pytest.mark.django_db
@override_settings(DEBUG=True)
def test_api_dogs_double_slash_returns_json_404():
    client = Client()
    res = client.get("/api/dogs//")
    assert res.status_code == 404
    assert res["Content-Type"].startswith("application/json")
    assert res.json()["code"] == "not_found"


@pytest.mark.django_db
@override_settings(DEBUG=True)
def test_non_api_404_still_html_in_debug():
    client = Client()
    res = client.get("/not-an-api-page/")
    assert res.status_code == 404
    assert "text/html" in res["Content-Type"]
