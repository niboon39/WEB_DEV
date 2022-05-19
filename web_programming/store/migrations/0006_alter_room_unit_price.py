# Generated by Django 4.0.3 on 2022-04-21 21:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_room_options_remove_booking_placed_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]