# Generated by Django 4.1.2 on 2022-11-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0002_alter_product_pic1_alter_product_pic2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buyer",
            name="pic",
            field=models.ImageField(default="", null=True, upload_to="upload"),
        ),
    ]
