# Generated by Django 3.0.3 on 2020-03-02 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newstraining', '0004_fndconfig_fndoutputs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fndconfig',
            old_name='fndOutputs',
            new_name='fndOutput',
        ),
    ]
