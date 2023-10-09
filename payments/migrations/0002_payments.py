# Generated by Django 4.2.4 on 2023-10-09 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(max_length=100)),
                ('idetification_type', models.CharField(max_length=10)),
                ('idetification_number', models.CharField(max_length=20)),
                ('payment_id', models.CharField(max_length=11)),
                ('description', models.CharField(max_length=100)),
                ('date_approved', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_of_expiration', models.DateTimeField(blank=True, null=True)),
                ('date_last_updated', models.DateTimeField(blank=True, null=True)),
                ('payment_method_id', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]