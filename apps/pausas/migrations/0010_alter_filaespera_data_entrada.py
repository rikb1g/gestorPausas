# Generated by Django 4.2.10 on 2024-10-04 08:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pausas", "0009_pausa_pausa_alter_filaespera_data_entrada"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filaespera",
            name="data_entrada",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 10, 4, 8, 34, 46, 20013, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
