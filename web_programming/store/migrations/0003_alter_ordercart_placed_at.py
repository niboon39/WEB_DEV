# Generated by Django 4.0.3 on 2022-04-01 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_ordercart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercart',
            name='placed_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
