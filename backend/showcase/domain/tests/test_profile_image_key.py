import pytest

from showcase.domain.exceptions import DomainValidationError
from showcase.domain.profile_image_key import ProfileImageKey


def test_profile_image_key_parse():
    k = ProfileImageKey.parse("  uploads/dogs/abc.webp  ")
    assert k.value == "uploads/dogs/abc.webp"


@pytest.mark.parametrize("raw", ["", "  ", "..", "/abs/path"])
def test_profile_image_key_rejects_invalid(raw: str):
    with pytest.raises(DomainValidationError):
        ProfileImageKey.parse(raw)
