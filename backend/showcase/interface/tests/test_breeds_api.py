import pytest
from django.test import Client

from showcase.models import Breed as BreedRow


@pytest.mark.django_db
def test_breeds_list_returns_items():
    BreedRow.objects.create(code=1, name="柴犬", sort_order=10)
    BreedRow.objects.create(code=2, name="秋田犬", sort_order=20)

    client = Client()
    res = client.get("/api/breeds/")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert len(data["items"]) == 2
    codes = {x["code"] for x in data["items"]}
    assert codes == {1, 2}


@pytest.mark.django_db
def test_breeds_post_method_not_allowed():
    client = Client()
    res = client.post("/api/breeds/", data={}, content_type="application/json")
    assert res.status_code == 405
    assert res.json()["code"] == "method_not_allowed"
