# Generated by Django 4.0.1 on 2022-03-14 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0052_polevoyworkreject_aktfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='polevoyworkreject',
            name='aktfile',
        ),
    ]