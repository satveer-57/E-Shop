# Generated by Django 4.1.2 on 2022-11-14 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0006_checkoutproducts_qty_checkoutproducts_total"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkout",
            name="total",
            field=models.IntegerField(default=0),
        ),
    ]
