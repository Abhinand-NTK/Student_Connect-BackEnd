# Generated by Django 5.0 on 2024-01-29 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_comment_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='comments',
            field=models.ManyToManyField(blank=True, to='blog.comment'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='likes',
            field=models.ManyToManyField(blank=True, to='blog.like'),
        ),
    ]
