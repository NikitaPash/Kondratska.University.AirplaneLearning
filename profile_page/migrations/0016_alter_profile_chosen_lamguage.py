# Generated by Django 5.0.3 on 2024-03-27 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_page', '0015_profile_chosen_lamguage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='chosen_lamguage',
            field=models.CharField(choices=[('English', 'English'), ('German', 'German'), ('Spanish', 'Spanish')], default='English', max_length=30),
        ),
    ]