"""Django ORM によるリポジトリ実装。"""

from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import IntegrityError

from showcase.domain.breed import Breed
from showcase.domain.dog import Dog
from showcase.domain.email import Email
from showcase.domain.exceptions import EmailAlreadyRegisteredError
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

    def is_email_registered(self, email: Email) -> bool:
        User = get_user_model()
        return User.objects.filter(username=email.value).exists()

    def register_with_password(self, owner: Owner, password: str) -> None:
        try:
            mappers.create_owner_with_password(owner, password)
        except IntegrityError as exc:
            raise EmailAlreadyRegisteredError from exc


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
    def delete_by_id_for_owner(self, owner_id: OwnerId, dog_id: UUID) -> int:
        """`Dog` テーブルで削除された行数（0 なら該当なし）。

        `QuerySet.delete()` の第1戻り値は CASCADE 先も含む総数のため使わない。
        第2戻り値のモデル別内訳で `Dog` のみを数える。論理削除に変える場合は
        `update(deleted_at=...)` 等に差し替え、戻り値の意味も合わせて変えること。
        """
        _total, per_model = DogRow.objects.filter(
            id=dog_id, owner_id=owner_id.value
        ).delete()
        return int(per_model.get(DogRow._meta.label, 0))

    def get_by_id(self, dog_id: UUID) -> Dog | None:
        try:
            row = DogRow.objects.select_related("breed", "owner").get(pk=dog_id)
        except DogRow.DoesNotExist:
            return None
        return mappers.dog_row_to_domain(row)

    def get_by_id_for_owner(self, owner_id: OwnerId, dog_id: UUID) -> Dog | None:
        try:
            row = DogRow.objects.select_related("breed", "owner").get(
                pk=dog_id, owner_id=owner_id.value
            )
        except DogRow.DoesNotExist:
            return None
        return mappers.dog_row_to_domain(row)

    def list_all_ordered(self) -> list[Dog]:
        qs = DogRow.objects.select_related("breed", "owner").order_by(
            "-created_at", "id"
        )
        return [mappers.dog_row_to_domain(r) for r in qs]

    def list_by_owner(self, owner_id: OwnerId) -> list[Dog]:
        qs = DogRow.objects.select_related("breed", "owner").filter(
            owner_id=owner_id.value
        )
        return [mappers.dog_row_to_domain(r) for r in qs]

    def save(self, dog: Dog) -> None:
        mappers.persist_dog(dog)
