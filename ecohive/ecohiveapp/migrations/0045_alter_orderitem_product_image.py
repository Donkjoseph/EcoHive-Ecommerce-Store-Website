# Generated by Django 4.2.4 on 2023-09-25 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecohiveapp', '0044_orderitem_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product_image',
            field=models.ImageField(upload_to='product_images/'),
        ),
    ]
