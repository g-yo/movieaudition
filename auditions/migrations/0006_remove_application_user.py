# Generated by Django 5.0.3 on 2024-08-29 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auditions', '0005_alter_application_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='user',
        ),
    ]
