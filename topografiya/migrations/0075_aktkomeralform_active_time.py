# Generated by Django 4.0.1 on 2022-03-25 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0074_workerobject_active_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='aktkomeralform',
            name='active_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
