# Generated by Django 4.1 on 2022-08-24 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_alter_employee_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.IntegerField(null=True),
        ),
    ]