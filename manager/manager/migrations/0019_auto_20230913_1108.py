# Generated by Django 2.2.28 on 2023-09-13 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0018_auto_20230228_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='content_kalite_en',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='content_kalite_es',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='content_kalite_fr',
        ),
    ]