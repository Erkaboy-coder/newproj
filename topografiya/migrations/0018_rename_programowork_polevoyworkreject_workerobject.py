# Generated by Django 4.0.1 on 2022-02-11 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0017_polevoyworkreject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='polevoyworkreject',
            old_name='programowork',
            new_name='workerobject',
        ),
    ]
