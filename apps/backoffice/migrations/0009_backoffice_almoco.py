# Generated by Django 5.1.1 on 2025-01-03 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0008_backoffice_data_aprovacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='backoffice',
            name='almoco',
            field=models.BooleanField(default=False),
        ),
    ]
