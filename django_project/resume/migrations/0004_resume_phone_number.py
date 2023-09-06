# Generated by Django 4.2 on 2023-06-05 17:16

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_resume_upload_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=20, null=True, region=None),
        ),
    ]