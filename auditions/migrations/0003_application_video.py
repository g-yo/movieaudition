# Generated by Django 5.0.3 on 2024-08-27 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditions', '0002_application_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
