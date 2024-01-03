# Generated by Django 5.0 on 2023-12-26 10:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0008_registercollege_primary_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registercollege',
            name='user_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]