# Generated by Django 3.0.2 on 2020-02-06 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newstraining", "0006_auto_20200206_0930"),
    ]

    operations = [
        migrations.AddField(
            model_name="fndrundetail",
            name="modelFileName",
            field=models.CharField(
                default="fnd_model_20200206-152441.h5", max_length=100
            ),
            preserve_default=False,
        ),
    ]