# Generated by Django 4.2.4 on 2023-09-06 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecohiveapp', '0013_remove_certification_certification_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='default_product_price',
        ),
    ]
