# Generated by Django 5.1.3 on 2024-11-27 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0004_alter_door_rooms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='door',
            name='rooms',
        ),
        migrations.RemoveField(
            model_name='room',
            name='capacity',
        ),
        migrations.AddField(
            model_name='room',
            name='door',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='apartments.door'),
        ),
    ]