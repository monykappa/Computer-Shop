# Generated by Django 5.0.6 on 2024-07-04 09:10

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_aboutus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutus',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
