# Generated by Django 5.0.3 on 2024-03-29 16:04

from django.db import migrations, models

import profile_page.models


class Migration(migrations.Migration):
    dependencies = [
        ('profile_page', '0022_alter_profile_profile_pic_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic_url',
            field=models.ImageField(default=profile_page.models.get_random_profile_pic, upload_to='uploads/'),
        ),
    ]
