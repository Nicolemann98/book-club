# Generated by Django 5.1 on 2024-11-18 15:13

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 11, 1)),
            preserve_default=False,
        ),
    ]