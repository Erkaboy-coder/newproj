# Generated by Django 4.0.1 on 2022-02-24 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0029_alter_programworkfiles_file1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programworkfiles',
            name='programworkform',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='programworkfilesss', to='topografiya.programworkform'),
        ),
    ]
