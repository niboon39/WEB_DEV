# Generated by Django 4.0.3 on 2022-04-21 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_room_unit_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['people']},
        ),
    ]
