# Generated by Django 4.0.1 on 2022-02-24 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0030_alter_programworkfiles_programworkform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programworkfiles',
            name='programworkform',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='programworkfiles', to='topografiya.programworkform'),
        ),
    ]
