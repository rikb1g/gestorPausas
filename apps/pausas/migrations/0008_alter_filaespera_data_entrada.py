# Generated by Django 5.1.1 on 2024-09-20 15:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pausas", "0007_pausa_data_aprovacao_alter_filaespera_data_entrada"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filaespera",
            name="data_entrada",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 9, 20, 15, 5, 8, 810187, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]