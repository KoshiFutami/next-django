import pytest

from showcase.domain.exceptions import DomainValidationError
from showcase.domain.handle import parse_optional_handle


def test_parse_optional_handle_strips_at_and_lowercases():
    assert parse_optional_handle("  @Foo_Bar  ") == "foo_bar"


def test_parse_optional_handle_none_and_empty():
    assert parse_optional_handle(None) is None
    assert parse_optional_handle("") is None
    assert parse_optional_handle("   ") is None
    assert parse_optional_handle("@") is None


@pytest.mark.parametrize(
    "raw",
    ["ab", "a" * 31, "ab!", "ab cd", "ab..c", "a@b"],
)
def test_parse_optional_handle_rejects_invalid(raw: str):
    with pytest.raises(DomainValidationError):
        parse_optional_handle(raw)


def test_parse_optional_handle_rejects_reserved():
    with pytest.raises(DomainValidationError, match="handle_reserved"):
        parse_optional_handle("admin")


def test_parse_optional_handle_accepts_valid():
    assert parse_optional_handle("pochi_2024") == "pochi_2024"
