# Generated by Django 5.1.5 on 2025-03-20 11:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Darkheka',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('keys', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/darkheka')),
            ],
        ),
    ]
