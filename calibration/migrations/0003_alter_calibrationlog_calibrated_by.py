# Generated by Django 5.1.5 on 2025-03-24 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calibration', '0002_alter_medicalequipment_calibration_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calibrationlog',
            name='calibrated_by',
            field=models.TextField(),
        ),
    ]
