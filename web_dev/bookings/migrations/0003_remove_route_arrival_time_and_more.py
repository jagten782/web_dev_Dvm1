# Generated by Django 4.2.19 on 2025-02-23 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0002_remove_bus_end_location_day_day_of_week_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="route",
            name="arrival_time",
        ),
        migrations.RemoveField(
            model_name="route",
            name="fare_multiplier",
        ),
        migrations.RemoveField(
            model_name="route",
            name="location",
        ),
        migrations.RemoveField(
            model_name="route",
            name="stop_order",
        ),
    ]
