# Generated by Django 4.0.1 on 2022-02-01 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0009_rename_object_programworkreject_programowork'),
    ]

    operations = [
        migrations.AddField(
            model_name='programworkreject',
            name='reason',
            field=models.TextField(blank=True),
        ),
    ]
