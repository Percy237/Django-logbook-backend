# Generated by Django 5.0.6 on 2024-06-01 13:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_logbookentry_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='logbookentry',
            name='created_by',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
