# Generated by Django 5.0.4 on 2024-04-23 14:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('modules', '0024_alter_lesson_sections'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='sections',
            field=models.ManyToManyField(related_name='lessons', to='modules.section'),
        ),
    ]
