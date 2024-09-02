# Generated by Django 5.0.7 on 2024-08-28 18:05

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
            name='User_Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('room_number', models.CharField(max_length=10)),
                ('bed_number', models.CharField(max_length=10)),
                ('mobile_number', models.CharField(max_length=15)),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics/')),
                ('aadhar_card', models.CharField(blank=True, max_length=12, null=True)),
                ('pan_card', models.CharField(blank=True, max_length=10, null=True)),
                ('bio', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
