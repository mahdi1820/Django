# Generated by Django 4.2.1 on 2023-05-21 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_remove_days_position_in_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='days',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
