# Generated by Django 5.0.1 on 2024-01-19 11:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_address_alter_otp_expiration_time_deliver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='otp',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 11, 13, 37, 237403, tzinfo=datetime.timezone.utc), editable=False),
        ),
    ]
