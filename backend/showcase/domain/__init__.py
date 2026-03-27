"""ドメイン層: エンティティ・値オブジェクト・集約・リポジトリ抽象。"""

from showcase.domain.breed import Breed
from showcase.domain.dog import Dog
from showcase.domain.email import Email
from showcase.domain.exceptions import DomainError, DomainValidationError
from showcase.domain.owner import Owner
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey
from showcase.domain.repositories import BreedRepository, OwnerRepository

__all__ = [
    "Breed",
    "BreedRepository",
    "Dog",
    "DomainError",
    "DomainValidationError",
    "Email",
    "Owner",
    "OwnerId",
    "OwnerRepository",
    "ProfileImageKey",
]
