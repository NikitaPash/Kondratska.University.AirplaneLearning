# Generated by Django 5.0.3 on 2024-03-30 14:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('profile_page', '0024_profile_chosen_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('alternate_title', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
    ]
