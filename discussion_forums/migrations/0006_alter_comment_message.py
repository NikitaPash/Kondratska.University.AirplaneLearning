# Generated by Django 5.0.4 on 2024-04-11 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion_forums', '0005_commentdeletionevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.TextField(max_length=500),
        ),
    ]