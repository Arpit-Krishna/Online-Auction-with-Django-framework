# Generated by Django 4.1.5 on 2023-01-13 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]
