# Generated by Django 4.1.7 on 2023-05-12 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_activities_grouplevel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activities',
            old_name='grouplevel',
            new_name='group',
        ),
    ]
