# Generated by Django 5.0.3 on 2024-09-27 18:20

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auditions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='age',
        ),
        migrations.AddField(
            model_name='application',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0)),
        ),
        migrations.AddField(
            model_name='application',
            name='selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='application',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
        migrations.AddField(
            model_name='movie',
            name='age_end',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='age_start',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='last_registration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 27, 18, 20, 17, 490962, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
