# Generated by Django 4.2 on 2023-06-13 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_rename_location_job_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='required_skills',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]