# Generated by Django 4.1.7 on 2023-05-05 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_attendance_cl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='id',
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=60, primary_key=True, serialize=False),
        ),
    ]
