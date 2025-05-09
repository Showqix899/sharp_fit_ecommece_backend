# Generated by Django 5.1.7 on 2025-04-06 20:00

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_default_device'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_used', models.BooleanField(default=False)),
                ('expires_at', models.DateTimeField()),
                ('admin', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_invites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
