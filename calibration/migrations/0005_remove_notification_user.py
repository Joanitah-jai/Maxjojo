# Generated by Django 5.1.5 on 2025-03-25 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calibration', '0004_medicalequipment_is_notified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
    ]
