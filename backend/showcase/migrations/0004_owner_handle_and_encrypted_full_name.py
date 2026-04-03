"""handle（必須化まで）と本名の Fernet 暗号（カラム名 full_name）を一括追加。"""

import uuid

from django.db import migrations, models


def forwards_fill_encrypted_full_name(apps, schema_editor):
    from showcase.infrastructure.pii_crypto import encrypt_pii

    OwnerProfile = apps.get_model("showcase", "OwnerProfile")
    placeholder = encrypt_pii("（本名未登録）")
    for row in OwnerProfile.objects.all():
        row.full_name = placeholder
        row.save(update_fields=["full_name"])


def forwards_assign_handles(apps, schema_editor):
    OwnerProfile = apps.get_model("showcase", "OwnerProfile")
    for row in OwnerProfile.objects.all():
        if row.handle:
            continue
        while True:
            candidate = "u" + uuid.uuid4().hex[:20]
            if not OwnerProfile.objects.filter(handle=candidate).exists():
                row.handle = candidate
                row.save(update_fields=["handle"])
                break


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    # PostgreSQL: 同一トランザクション内で RunPython の UPDATE の直後に ALTER すると
    # 「pending trigger events」で失敗することがあるため、操作ごとにコミットする。
    atomic = False

    dependencies = [
        ("showcase", "0003_dog_name_plaintext"),
    ]

    operations = [
        migrations.AddField(
            model_name="ownerprofile",
            name="handle",
            field=models.CharField(
                blank=True,
                help_text="公開ハンドル（小文字・@ なし、一意）",
                max_length=30,
                null=True,
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="ownerprofile",
            name="full_name",
            field=models.TextField(
                help_text="本名の Fernet 暗号文（平文はアプリ内のみ）",
                null=True,
            ),
        ),
        migrations.RunPython(forwards_fill_encrypted_full_name, noop_reverse),
        migrations.RunPython(forwards_assign_handles, noop_reverse),
        migrations.AlterField(
            model_name="ownerprofile",
            name="full_name",
            field=models.TextField(
                help_text="本名の Fernet 暗号文（平文はアプリ内のみ）",
            ),
        ),
        migrations.AlterField(
            model_name="ownerprofile",
            name="handle",
            field=models.CharField(
                help_text="公開ハンドル（小文字・@ なし、一意・必須）",
                max_length=30,
                unique=True,
            ),
        ),
    ]
