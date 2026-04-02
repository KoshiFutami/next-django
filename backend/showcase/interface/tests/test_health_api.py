import pytest
from django.test import Client


@pytest.mark.django_db
def test_health_returns_ok():
    client = Client()
    res = client.get("/api/health/")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
