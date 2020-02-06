# Generated by Django 3.0.2 on 2020-02-06 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newstraining', '0004_fndinput_trainingindicator'),
    ]

    operations = [
        migrations.CreateModel(
            name='FNDRunDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runStartTime', models.DateTimeField()),
                ('runEndTime', models.DateTimeField()),
                ('historyStartTime', models.DateTimeField()),
                ('historyEndTime', models.DateTimeField()),
                ('fndConfig', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newstraining.FNDConfig')),
            ],
        ),
    ]
