# Generated by Django 4.0.1 on 2022-02-17 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0024_alter_leaderkomeralworkreject_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='topografiya/static/files/otchot', verbose_name='Report file')),
                ('reason', models.TextField(blank=True)),
                ('status', models.IntegerField(default=0)),
                ('active_time', models.DateTimeField(auto_now=True, null=True)),
                ('object', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='objectreport', to='topografiya.object')),
            ],
            options={
                'verbose_name_plural': 'Report',
            },
        ),
    ]
