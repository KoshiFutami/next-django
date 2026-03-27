"""永続化の抽象（実装は infrastructure）。"""

from typing import Protocol

from showcase.domain.breed import Breed
from showcase.domain.email import Email
from showcase.domain.owner import Owner
from showcase.domain.owner_id import OwnerId


class OwnerRepository(Protocol):
    def get_by_id(self, owner_id: OwnerId) -> Owner | None: ...
    def get_by_email(self, email: Email) -> Owner | None: ...
    def save(self, owner: Owner) -> None: ...


class BreedRepository(Protocol):
    """犬種マスタ。主キーは code（int）。"""

    def get_by_code(self, code: int) -> Breed | None: ...
    def list_ordered(self) -> list[Breed]: ...
    def save(self, breed: Breed) -> None: ...
