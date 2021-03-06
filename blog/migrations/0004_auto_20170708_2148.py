# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-09 01:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170708_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='tags',
        ),
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(default='python', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_query_name='tag', to='blog.Post'),
            preserve_default=False,
        ),
    ]
