# Generated by Django 3.0.2 on 2020-02-08 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newstraining", "0007_fndrundetail_modelfilename"),
    ]

    operations = [
        migrations.AddField(
            model_name="fndrundetail",
            name="gloveFileLocation",
            field=models.CharField(default=0, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="fndrundetail",
            name="tokenizerFileName",
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]