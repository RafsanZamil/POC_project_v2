# Generated by Django 5.0.2 on 2024-03-04 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0004_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
