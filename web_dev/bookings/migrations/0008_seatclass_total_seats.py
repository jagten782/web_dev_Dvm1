# Generated by Django 4.2.19 on 2025-02-25 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0007_alter_day_day_of_week_remove_seatclass_day_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="seatclass",
            name="total_seats",
            field=models.IntegerField(default=0),
        ),
    ]
