from datetime import datetime, timezone
from uuid import UUID

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from showcase.domain.email import Email
from showcase.infrastructure.pii_crypto import (
    email_login_username,
    encrypt_pii,
)
from showcase.models import OwnerProfile


class Command(BaseCommand):
    help = "SHOWCASE_STUB_OWNER_ID に対応する stub OwnerProfile を投入/更新する"

    def handle(self, *args, **options):
        stub_owner_id = UUID(str(settings.SHOWCASE_STUB_OWNER_ID))
        email_raw = settings.SHOWCASE_STUB_OWNER_EMAIL
        email_vo = Email.parse(str(email_raw))
        login_uname = email_login_username(email_vo)
        nickname = "スタブオーナー"

        User = get_user_model()
        user, user_created = User.objects.get_or_create(
            username=login_uname,
            defaults={"email": ""},
        )

        _, owner_created = OwnerProfile.objects.update_or_create(
            id=stub_owner_id,
            defaults={
                "user": user,
                "nickname": nickname,
                "pii_email_ciphertext": encrypt_pii(email_vo.value),
                "profile_image_key": None,
                "created_at": datetime.now(timezone.utc),
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "seed_stub_owner completed: "
                f"user_created={user_created}, owner_created={owner_created}, owner_id={stub_owner_id}"
            )
        )
