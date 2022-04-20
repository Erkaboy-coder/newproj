# Generated by Django 4.0.1 on 2022-04-19 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0084_branch1'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Branch1',
        ),
        migrations.AlterField(
            model_name='pdowork',
            name='department',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='workdepartment', to='topografiya.department'),
        ),
        migrations.AlterField(
            model_name='pdowork',
            name='work_term',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='workperiod', to='topografiya.period'),
        ),
        migrations.AlterField(
            model_name='pdowork',
            name='work_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='workptype', to='topografiya.worktype'),
        ),
    ]
