# Generated by Django 3.1 on 2021-06-03 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='print',
            new_name='price',
        ),
    ]
