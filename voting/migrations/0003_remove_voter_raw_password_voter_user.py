# Generated by Django 5.1.2 on 2024-11-13 08:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0002_voter_raw_password'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voter',
            name='raw_password',
        ),
        migrations.AddField(
            model_name='voter',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voter', to=settings.AUTH_USER_MODEL),
        ),
    ]
