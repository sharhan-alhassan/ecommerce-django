# Generated by Django 3.1 on 2021-06-29 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210629_1507'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingaddress',
            old_name='countries',
            new_name='country',
        ),
    ]
