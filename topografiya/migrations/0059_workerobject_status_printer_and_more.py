# Generated by Django 4.0.1 on 2022-03-15 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0058_leaderkomeralworkreject_rejected_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workerobject',
            name='status_printer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='workerobject',
            name='status_repoert_printer',
            field=models.IntegerField(default=0),
        ),
    ]
