# Generated by Django 4.2.1 on 2023-05-20 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_alter_teacherextra_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherextra',
            name='groups',
            field=models.ManyToManyField(blank=True, to='home.group'),
        ),
    ]
