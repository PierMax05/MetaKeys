# Generated by Django 5.1.3 on 2024-12-05 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0014_remove_apartmentinfo_apartments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentinfo',
            name='apartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apartment_info', to='apartments.apartment'),
        ),
    ]