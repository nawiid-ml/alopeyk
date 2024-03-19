# Generated by Django 5.0 on 2024-03-01 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_latitude', models.DecimalField(decimal_places=6, max_digits=20)),
                ('origin_longitude', models.DecimalField(decimal_places=6, max_digits=20)),
                ('destination_latitude', models.DecimalField(decimal_places=6, max_digits=20)),
                ('destination_longitude', models.DecimalField(decimal_places=6, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
