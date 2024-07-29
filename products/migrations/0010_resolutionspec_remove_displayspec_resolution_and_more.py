# Generated by Django 5.0.6 on 2024-07-29 03:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_displayspec_resolution'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResolutionSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('resolution', models.CharField(blank=True, choices=[('HD', 'HD'), ('Full HD', 'Full HD'), ('2K', '2K'), ('4K', '4K')], max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='displayspec',
            name='resolution',
        ),
        migrations.AddField(
            model_name='laptopspec',
            name='resolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.resolutionspec'),
        ),
    ]
