# Generated by Django 3.2.7 on 2022-01-04 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plate', '0002_plate_save_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plate',
            old_name='is_avtive',
            new_name='is_active',
        ),
    ]