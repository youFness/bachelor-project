# Generated by Django 4.2 on 2023-06-13 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='skills',
        ),
    ]
