# Generated by Django 4.1 on 2022-08-18 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='role',
            new_name='userProfile',
        ),
    ]
