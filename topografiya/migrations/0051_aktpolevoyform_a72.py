# Generated by Django 4.0.1 on 2022-03-14 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0050_aktpolevoyform_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='aktpolevoyform',
            name='a72',
            field=models.TextField(blank=True),
        ),
    ]