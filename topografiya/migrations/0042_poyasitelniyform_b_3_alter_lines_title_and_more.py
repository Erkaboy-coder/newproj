# Generated by Django 4.0.1 on 2022-03-02 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0041_polygons_points_lines'),
    ]

    operations = [
        migrations.AddField(
            model_name='poyasitelniyform',
            name='b_3',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='lines',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='points',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='polygons',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
