# Generated by Django 4.0.1 on 2022-02-13 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0020_alter_aktkomeralform_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aktkomeralform',
            old_name='workerobject',
            new_name='object',
        ),
    ]