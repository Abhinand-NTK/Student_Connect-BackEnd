# Generated by Django 5.0 on 2024-01-16 04:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeadmin', '0028_staff_user_id_student_user_id'),
        ('staffuser', '0003_alter_classroom_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoomForTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='staffuser.classroom')),
                ('staff_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='collegeadmin.staff')),
                ('sub_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='collegeadmin.subject')),
            ],
        ),
    ]