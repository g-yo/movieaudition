# Generated by Django 5.0.3 on 2024-09-27 03:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditions', '0012_alter_movie_last_registration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='last_registration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 27, 3, 10, 52, 630991, tzinfo=datetime.timezone.utc)),
        ),
    ]
