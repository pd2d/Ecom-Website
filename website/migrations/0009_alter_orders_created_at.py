# Generated by Django 4.2.5 on 2023-10-03 03:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_alter_orders_created_at_alter_orders_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 3, 3, 51, 15, 1370, tzinfo=datetime.timezone.utc)),
        ),
    ]
