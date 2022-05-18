# Generated by Django 4.0.1 on 2022-04-22 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0086_remove_pdowork_department_alter_pdowork_work_term_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='department',
        ),
        migrations.AddField(
            model_name='worker',
            name='subdivision',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='workersubdivision', to='topografiya.subdivisions'),
            preserve_default=False,
        ),
    ]