# Generated by Django 5.0.2 on 2024-03-19 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_product_delete_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='user',
            new_name='owner',
        ),
    ]
