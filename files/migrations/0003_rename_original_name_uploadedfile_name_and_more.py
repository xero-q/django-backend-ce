# Generated by Django 5.1.1 on 2024-09-14 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_alter_uploadedfile_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadedfile',
            old_name='original_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='uploadedfile',
            name='new_name',
        ),
    ]
