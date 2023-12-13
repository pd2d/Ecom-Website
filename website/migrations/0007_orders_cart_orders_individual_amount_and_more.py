# Generated by Django 4.2.5 on 2023-10-02 18:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_remove_products_stock_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='cart',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='website.cart'),
        ),
        migrations.AddField(
            model_name='orders',
            name='individual_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='orders',
            name='number_of_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='orders',
            name='status_of_payment',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='orders',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 2, 18, 35, 44, 428322, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='orders',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.products'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
