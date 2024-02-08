# Generated by Django 4.0 on 2024-02-08 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_blogpost_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='comments',
            field=models.ManyToManyField(blank=True, to='blog.Comment'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='likes',
            field=models.ManyToManyField(blank=True, to='blog.Like'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag'),
        ),
    ]
