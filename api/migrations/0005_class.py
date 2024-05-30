# Generated by Django 5.0.6 on 2024-05-29 13:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('courses', models.ManyToManyField(related_name='class_courses', to='api.course')),
                ('students', models.ManyToManyField(related_name='classes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]