# Generated by Django 4.0.1 on 2022-02-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0014_aktkomeralform_a10'),
    ]

    operations = [
        migrations.AddField(
            model_name='aktpolevoyform',
            name='a10',
            field=models.TextField(blank=True),
        ),
    ]
