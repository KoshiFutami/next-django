import uuid

from django.conf import settings
from django.db import models


class OwnerProfile(models.Model):
    """ドメイン Owner と 1:1。id は OwnerId.value と一致させる。"""

    id = models.UUIDField(primary_key=True, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owner_profile",
    )
    nickname = models.CharField(max_length=64)
    full_name = models.CharField(
        max_length=128,
        blank=True,
        default="",
        help_text="本名（任意）",
    )
    handle = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        help_text="公開ハンドル（小文字・@ なし、一意）",
    )
    pii_email_ciphertext = models.TextField(
        blank=True,
        null=True,
        help_text="正規化済みメールの Fernet 暗号文（平文は User に保存しない）",
    )
    profile_image_key = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField()


class Breed(models.Model):
    """犬種マスタ。主キーは code（正の整数）。"""

    code = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "code"]


class Dog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        OwnerProfile,
        on_delete=models.CASCADE,
        related_name="dogs",
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.PROTECT,
        to_field="code",
        db_column="breed_code",
    )
    name = models.CharField(max_length=128)
    birth_date = models.DateField()
    weight = models.FloatField()
    color = models.CharField(max_length=64)
    gender = models.CharField(max_length=32)
    profile_image_key = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]
