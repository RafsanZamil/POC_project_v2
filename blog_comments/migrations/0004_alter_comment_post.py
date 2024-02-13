# Generated by Django 5.0.2 on 2024-02-13 08:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_comments', '0003_alter_comment_comment_author'),
        ('blogs', '0004_alter_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogs.post'),
        ),
    ]