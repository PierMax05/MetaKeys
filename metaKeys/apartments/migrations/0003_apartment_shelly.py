# Generated by Django 5.1.4 on 2024-12-29 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='shelly',
            field=models.BooleanField(default=False),
        ),
    ]
