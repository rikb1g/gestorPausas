# Generated by Django 5.1.1 on 2024-09-19 21:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backoffice", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="backofficefilaespera",
            name="data_entrada",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 9, 19, 21, 21, 44, 676220, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
