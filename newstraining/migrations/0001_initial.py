# Generated by Django 3.0.3 on 2020-03-01 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FNDConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fndType', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FNDInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variableName', models.CharField(max_length=100)),
                ('variableSymbol', models.CharField(max_length=100)),
                ('trainingIndicator', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='FNDModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('algorithm', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FNDOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variableName', models.CharField(max_length=100)),
                ('variableSymbol', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='JobTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeName', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('expression', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FNDRunDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runStartTime', models.DateTimeField()),
                ('runEndTime', models.DateTimeField()),
                ('historyStartTime', models.DateTimeField(null=True)),
                ('historyEndTime', models.DateTimeField(null=True)),
                ('modelFileName', models.CharField(max_length=100)),
                ('tokenizerFileName', models.CharField(max_length=100)),
                ('fndConfig', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newstraining.FNDConfig')),
            ],
        ),
        migrations.CreateModel(
            name='FNDModelAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('fndModel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newstraining.FNDModel')),
            ],
        ),
        migrations.AddField(
            model_name='fndconfig',
            name='fndInput',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='newstraining.FNDInput'),
        ),
        migrations.AddField(
            model_name='fndconfig',
            name='fndModel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newstraining.FNDModel'),
        ),
    ]
