# Generated by Django 5.0.6 on 2024-07-09 03:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryassignment',
            name='status',
        ),
        migrations.AlterField(
            model_name='deliveryassignment',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_assignment', to='orders.orderhistory'),
        ),
    ]
