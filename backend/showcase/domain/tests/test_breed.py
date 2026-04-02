import pytest

from showcase.domain.breed import Breed
from showcase.domain.exceptions import DomainValidationError


def test_breed_create():
    b = Breed.create(code=101, name=" 柴犬 ")
    assert b.code == 101
    assert b.name == "柴犬"


def test_breed_rejects_invalid_code():
    with pytest.raises(DomainValidationError, match="breed_code_invalid"):
        Breed.create(code=0, name="x")
    with pytest.raises(DomainValidationError, match="breed_code_invalid"):
        Breed.create(code=-1, name="x")


@pytest.mark.parametrize("name", ["", "  "])
def test_breed_rejects_empty_name(name: str):
    with pytest.raises(DomainValidationError, match="breed_name_empty"):
        Breed.create(code=1, name=name)


def test_breed_rejects_negative_sort_order():
    with pytest.raises(DomainValidationError, match="breed_sort_order_negative"):
        Breed.create(code=1, name="y", sort_order=-1)
