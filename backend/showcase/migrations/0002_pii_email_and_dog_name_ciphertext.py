import re

from django.db import migrations, models


def forwards_encrypt_legacy(apps, schema_editor):
    from showcase.domain.email import Email
    from showcase.domain.exceptions import DomainValidationError
    from showcase.infrastructure.pii_crypto import (
        decrypt_pii,
        email_login_username,
        encrypt_pii,
    )

    User = apps.get_model("auth", "User")
    OwnerProfile = apps.get_model("showcase", "OwnerProfile")
    Dog = apps.get_model("showcase", "Dog")

    hmac_username = re.compile(r"^[0-9a-f]{64}$")

    for user in User.objects.all():
        un = user.username or ""
        if hmac_username.fullmatch(un):
            continue
        email_plain = (user.username or user.email or "").strip()
        if not email_plain or "@" not in email_plain:
            continue
        try:
            e = Email.parse(email_plain)
        except DomainValidationError:
            continue
        cipher = encrypt_pii(e.value)
        user.username = email_login_username(e)
        user.email = ""
        user.save(update_fields=["username", "email"])
        OwnerProfile.objects.filter(user_id=user.pk).update(pii_email_ciphertext=cipher)

    for dog in Dog.objects.all():
        raw = dog.name or ""
        if not raw:
            continue
        try:
            decrypt_pii(raw)
        except Exception:
            dog.name = encrypt_pii(raw)
            dog.save(update_fields=["name"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("showcase", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ownerprofile",
            name="pii_email_ciphertext",
            field=models.TextField(
                blank=True,
                help_text="正規化済みメールの Fernet 暗号文（平文は User に保存しない）",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="dog",
            name="name",
            field=models.TextField(help_text="愛犬名の Fernet 暗号文"),
        ),
        migrations.RunPython(forwards_encrypt_legacy, noop_reverse),
    ]
