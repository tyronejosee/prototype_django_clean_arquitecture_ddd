# Generated by Django 4.2.23 on 2025-06-30 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorymodel',
            name='image',
        ),
        migrations.RemoveField(
            model_name='categorymodel',
            name='parent',
        ),
    ]
