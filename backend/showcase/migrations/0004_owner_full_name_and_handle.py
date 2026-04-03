from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showcase", "0003_dog_name_plaintext"),
    ]

    operations = [
        migrations.AddField(
            model_name="ownerprofile",
            name="full_name",
            field=models.CharField(
                blank=True,
                default="",
                help_text="本名（任意）",
                max_length=128,
            ),
        ),
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
    ]
