# Generated by Django 5.0.2 on 2024-03-05 06:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_comments', '0006_alter_comment_post'),
        ('feed', '0006_delete_reactcomment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReactComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.CharField(choices=[('H', 'HAHA'), ('S', 'SAD'), ('C', 'CARE')], max_length=1)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_comments.comment')),
                ('reacted_by', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
