# Generated by Django 4.0.1 on 2022-01-31 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_product_size_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.TextField(default='BIG', null=True),
        ),
    ]