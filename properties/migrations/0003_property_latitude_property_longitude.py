# Generated by Django 5.1.1 on 2024-10-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0002_propertyimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="latitude",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=9, null=True
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="longitude",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=9, null=True
            ),
        ),
    ]
