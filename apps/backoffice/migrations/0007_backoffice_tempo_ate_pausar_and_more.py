# Generated by Django 5.1.1 on 2024-10-24 23:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backoffice", "0006_backoffice_inicio_pausa_backoffice_termo_pausa_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="backoffice",
            name="tempo_ate_pausar",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="backofficefilaespera",
            name="data_entrada",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]