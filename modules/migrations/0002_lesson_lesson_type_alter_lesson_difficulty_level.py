# Generated by Django 5.0.3 on 2024-03-16 22:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_type',
            field=models.CharField(choices=[('I', 'Informational'), ('Q', 'Quiz')], default='I', max_length=10),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='difficulty_level',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='easy',
                                   max_length=20),
        ),
    ]
