# Generated by Django 5.1.5 on 2025-02-18 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0002_delete_backofficenps_delete_frontofficenps_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('arquivo', models.FileField(upload_to='uploads/')),
                ('data_upload', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
