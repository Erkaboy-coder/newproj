# Generated by Django 4.0.1 on 2022-01-24 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topografiya', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Order_receiver',
            new_name='order_receiver',
        ),
    ]