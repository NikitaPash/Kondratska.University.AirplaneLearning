# Generated by Django 5.0.3 on 2024-04-02 18:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('modules', '0020_alter_quiz_difficulty_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='difficulty_level',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Easy',
                                   max_length=20),
        ),
    ]
