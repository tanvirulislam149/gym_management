# Generated by Django 5.2 on 2025-04-27 07:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookings', '0001_initial'),
        ('plans', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='book_fitness_classes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_classes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book_plans',
            name='plans',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='plans.plans'),
        ),
        migrations.AddField(
            model_name='book_plans',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='booked_plan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment_plans',
            name='booked_plans',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_status', to='bookings.book_plans'),
        ),
    ]
