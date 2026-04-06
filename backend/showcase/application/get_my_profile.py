from showcase.domain.owner import Owner
from showcase.domain.owner_id import OwnerId
from showcase.domain.repositories import OwnerRepository


class GetMyProfileUseCase:
    def __init__(self, owner_repository: OwnerRepository):
        self.owner_repository = owner_repository

    def execute(self, owner_id: OwnerId) -> Owner | None:
        return self.owner_repository.get_by_id(owner_id)
