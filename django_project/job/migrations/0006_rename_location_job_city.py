# Generated by Django 4.2 on 2023-05-22 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_industry_state_job_job_type_alter_applyjob_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='location',
            new_name='city',
        ),
    ]
