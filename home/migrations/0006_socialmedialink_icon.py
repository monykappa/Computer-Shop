# Generated by Django 5.0.6 on 2024-06-30 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_socialmedialink_delete_footer'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmedialink',
            name='icon',
            field=models.CharField(blank=True, help_text='FontAwesome icon class', max_length=50, null=True),
        ),
    ]
