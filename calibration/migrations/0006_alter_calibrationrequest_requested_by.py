# Generated by Django 5.1.5 on 2025-03-25 19:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calibration', '0005_remove_notification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calibrationrequest',
            name='requested_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_calibrations', to=settings.AUTH_USER_MODEL),
        ),
    ]
