import pytest
from django.db import DatabaseError
from django.test import Client

from showcase.interface import views


@pytest.mark.django_db
def test_health_returns_ok():
    client = Client()
    res = client.get("/api/health/")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


@pytest.mark.django_db
def test_health_returns_503_when_db_unavailable(monkeypatch):
    def raise_db_error(*_args, **_kwargs):
        raise DatabaseError("db down")

    monkeypatch.setattr(views.connection, "cursor", raise_db_error)

    client = Client()
    res = client.get("/api/health/")
    assert res.status_code == 503
    assert res.json()["code"] == "service_unavailable"
