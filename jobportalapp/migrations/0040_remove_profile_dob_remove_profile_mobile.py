# Generated by Django 4.2.1 on 2024-07-07 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportalapp', '0039_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='mobile',
        ),
    ]