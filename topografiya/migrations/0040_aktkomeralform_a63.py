# Generated by Django 4.0.1 on 2022-02-28 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0039_remove_aktkomeralform_a63_remove_aktkomeralform_a64'),
    ]

    operations = [
        migrations.AddField(
            model_name='aktkomeralform',
            name='a63',
            field=models.TextField(blank=True),
        ),
    ]