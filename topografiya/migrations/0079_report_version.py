# Generated by Django 4.0.1 on 2022-04-01 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0078_alter_programworkform_program_work_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='version',
            field=models.IntegerField(default=0),
        ),
    ]
