# Generated by Django 5.1.5 on 2025-02-09 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0006_remove_bus_fare"),
    ]

    operations = [
        migrations.AddField(
            model_name="intermediatestop",
            name="fare_multiplier",
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=5),
        ),
    ]
