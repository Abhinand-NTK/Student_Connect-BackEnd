# Generated by Django 5.0 on 2024-01-07 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeadmin', '0024_subject_semseter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='semseter',
            field=models.IntegerField(null=True),
        ),
    ]
