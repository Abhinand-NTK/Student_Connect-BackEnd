# Generated by Django 5.0 on 2024-01-26 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blogpost_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(to='blog.tag'),
        ),
    ]
