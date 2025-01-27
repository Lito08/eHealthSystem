# Generated by Django 5.1.5 on 2025-01-26 11:45

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact_info', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_id', models.CharField(default='DEFAULT_APPT', max_length=50, unique=True)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField(default=datetime.time(12, 0))),
                ('result', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Confirmed', 'Confirmed')], default='Scheduled', max_length=20)),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.clinic')),
            ],
        ),
    ]
