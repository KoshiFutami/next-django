"""Django ORM によるリポジトリ実装。"""

from uuid import UUID

from django.contrib.auth import get_user_model

from showcase.domain.breed import Breed
from showcase.domain.dog import Dog
from showcase.domain.email import Email
from showcase.domain.owner import Owner
from showcase.domain.owner_id import OwnerId
from showcase.infrastructure import mappers
from showcase.models import Breed as BreedRow
from showcase.models import Dog as DogRow
from showcase.models import OwnerProfile as OwnerProfileRow


class DjangoOwnerRepository:
    def get_by_id(self, owner_id: OwnerId) -> Owner | None:
        try:
            row = OwnerProfileRow.objects.select_related("user").get(pk=owner_id.value)
        except OwnerProfileRow.DoesNotExist:
            return None
        return mappers.owner_profile_to_domain(row)

    def get_by_email(self, email: Email) -> Owner | None:
        User = get_user_model()
        try:
            user = User.objects.get(username=email.value)
        except User.DoesNotExist:
            return None
        row = OwnerProfileRow.objects.filter(user=user).first()
        if row is None:
            return None
        return mappers.owner_profile_to_domain(row)

    def save(self, owner: Owner) -> None:
        mappers.persist_owner(owner)


class DjangoBreedRepository:
    def get_by_code(self, code: int) -> Breed | None:
        try:
            row = BreedRow.objects.get(pk=code)
        except BreedRow.DoesNotExist:
            return None
        return mappers.breed_row_to_domain(row)

    def list_ordered(self) -> list[Breed]:
        return [mappers.breed_row_to_domain(r) for r in BreedRow.objects.all()]

    def save(self, breed: Breed) -> None:
        mappers.persist_breed(breed)


class DjangoDogRepository:
    def get_by_id(self, dog_id: UUID) -> Dog | None:
        try:
            row = DogRow.objects.select_related("breed", "owner").get(pk=dog_id)
        except DogRow.DoesNotExist:
            return None
        return mappers.dog_row_to_domain(row)

    def list_by_owner(self, owner_id: OwnerId) -> list[Dog]:
        qs = DogRow.objects.select_related("breed", "owner").filter(
            owner_id=owner_id.value
        )
        return [mappers.dog_row_to_domain(r) for r in qs]

    def save(self, dog: Dog) -> None:
        mappers.persist_dog(dog)
