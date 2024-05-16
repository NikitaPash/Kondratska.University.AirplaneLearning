# Generated by Django 5.0.3 on 2024-03-21 22:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('profile_page', '0010_alter_profile_learner_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='learner_type',
            field=models.CharField(choices=[('A rookie!', 'Beginner'), ('A smart cookie!', 'Skilled'),
                                            ('A very smart cookie!', 'Advanced')], default='An avid learner!',
                                   max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='progress',
            field=models.FloatField(default=0),
        ),
    ]
