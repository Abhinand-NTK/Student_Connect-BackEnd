# Generated by Django 4.0 on 2024-02-09 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeadmin', '0038_alter_student_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='semester',
            field=models.CharField(blank=True, default='ancadf', max_length=30),
            preserve_default=False,
        ),
    ]
