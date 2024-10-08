# Generated by Django 5.1.1 on 2024-09-11 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UploadedFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="uploads/")),
                ("original_name", models.CharField(max_length=255)),
                ("new_name", models.CharField(blank=True, max_length=255, null=True)),
                ("size", models.PositiveIntegerField()),
                ("status", models.CharField(default="uploaded", max_length=50)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
