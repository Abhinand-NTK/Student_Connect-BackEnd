# Generated by Django 5.0 on 2023-12-26 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0009_alter_registercollege_user_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registercollege',
            name='primary_password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
