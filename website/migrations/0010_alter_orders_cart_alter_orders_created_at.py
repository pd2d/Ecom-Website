# Generated by Django 4.2.5 on 2023-10-03 03:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_alter_orders_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.cart'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 3, 3, 58, 45, 705130, tzinfo=datetime.timezone.utc)),
        ),
    ]
