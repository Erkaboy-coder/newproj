# Generated by Django 4.0.1 on 2022-02-15 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0022_leaderworkreject'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LeaderWorkReject',
            new_name='LeaderKomeralWorkReject',
        ),
        migrations.AddField(
            model_name='workerobject',
            name='status_geodezis_komeral',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='leaderkomeralworkreject',
            name='object',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='leaderkomeralworkreject', to='topografiya.object'),
        ),
    ]