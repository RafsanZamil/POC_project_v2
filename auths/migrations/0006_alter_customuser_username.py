# Generated by Django 5.0.2 on 2024-03-20 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0005_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(unique=True),
        ),
    ]
