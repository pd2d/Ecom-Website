# Generated by Django 4.2.5 on 2023-10-02 18:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_orders_cart_orders_individual_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 2, 18, 37, 8, 892595, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.products'),
        ),
    ]