# Generated by Django 5.0.6 on 2024-07-23 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_displayspec_refresh_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='displayspec',
            name='refresh_rate',
        ),
    ]