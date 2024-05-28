# Generated by Django 5.0.3 on 2024-04-02 17:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('modules', '0018_remove_quizuseranswers_answer'),
        ('profile_page', '0026_alter_profile_learner_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='chosen_language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='modules.language'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='learner_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='profile_page.learnertype'),
        ),
    ]
