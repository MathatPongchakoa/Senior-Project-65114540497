# Generated by Django 5.1.3 on 2024-12-07 06:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tableapp', '0006_rename_table_name_booking_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(default='2024-01-01'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_time',
            field=models.TimeField(default='12:00:00'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
