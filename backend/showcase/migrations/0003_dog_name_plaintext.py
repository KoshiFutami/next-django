from django.db import migrations, models


def forwards_decrypt_dog_names(apps, schema_editor):
    from showcase.infrastructure.pii_crypto import decrypt_pii

    Dog = apps.get_model("showcase", "Dog")
    for dog in Dog.objects.all():
        raw = dog.name or ""
        if not raw:
            continue
        try:
            plain = decrypt_pii(raw)
        except Exception:
            continue
        dog.name = plain
        dog.save(update_fields=["name"])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("showcase", "0002_pii_email_and_dog_name_ciphertext"),
    ]

    operations = [
        migrations.RunPython(forwards_decrypt_dog_names, noop_reverse),
        migrations.AlterField(
            model_name="dog",
            name="name",
            field=models.CharField(max_length=128),
        ),
    ]
