# Generated by Django 5.0.6 on 2024-07-22 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_userpreferences'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserPreferences',
        ),
    ]
