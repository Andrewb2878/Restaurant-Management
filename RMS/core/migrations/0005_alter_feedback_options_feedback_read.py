# Generated by Django 4.2.20 on 2025-05-09 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_feedback'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Feedback', 'verbose_name_plural': 'Feedback'},
        ),
        migrations.AddField(
            model_name='feedback',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
