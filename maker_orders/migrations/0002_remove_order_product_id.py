# Generated by Django 3.2.2 on 2021-05-09 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maker_orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product_id',
        ),
    ]
