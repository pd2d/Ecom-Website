# Generated by Django 4.2.4 on 2023-08-11 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_products_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='size',
            field=models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('extra_large', 'Extra_Large')], max_length=20),
        ),
    ]
