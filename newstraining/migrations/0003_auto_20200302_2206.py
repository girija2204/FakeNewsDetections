# Generated by Django 3.0.3 on 2020-03-02 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newstraining', '0002_auto_20200302_2205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fndconfig',
            old_name='fndInput',
            new_name='fndInputs',
        ),
    ]