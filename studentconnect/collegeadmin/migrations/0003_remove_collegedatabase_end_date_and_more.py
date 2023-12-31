# Generated by Django 5.0 on 2023-12-31 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeadmin', '0002_department_session_subject_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collegedatabase',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='collegedatabase',
            name='register_no',
        ),
        migrations.RemoveField(
            model_name='collegedatabase',
            name='start_date',
        ),
        migrations.AddField(
            model_name='collegedatabase',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='collegeadmin.collegedatabase')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collegeadmin.session')),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='collegeadmin.collegedatabase')),
            ],
        ),
    ]
