# Generated by Django 4.0.1 on 2022-02-25 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0032_remove_aktpolevoyform_a104'),
    ]

    operations = [
        migrations.AddField(
            model_name='aktpolevoyform',
            name='a104',
            field=models.TextField(blank=True),
        ),
    ]
