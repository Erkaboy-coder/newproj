# Generated by Django 4.0.1 on 2022-02-17 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0023_rename_leaderworkreject_leaderkomeralworkreject_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaderkomeralworkreject',
            options={'verbose_name_plural': 'LeaderKomeralWorkReject'},
        ),
        migrations.AlterField(
            model_name='worker',
            name='status',
            field=models.CharField(choices=[('0', 'Ishchi'), ('1', "Bo'lim boshlig'i"), ('2', 'Geodezis'), ('3', 'Ogogd'), ('4', 'Ogogd 2')], default='0', max_length=10, verbose_name='Ishchi'),
        ),
    ]
