# Generated by Django 4.2.19 on 2025-02-15 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0010_booking_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="travelling_class",
            field=models.CharField(default="none", max_length=100),
        ),
    ]
