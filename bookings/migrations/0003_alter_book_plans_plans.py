# Generated by Django 5.2 on 2025-05-28 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_initial'),
        ('plans', '0004_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_plans',
            name='plans',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plans.plans'),
        ),
    ]
