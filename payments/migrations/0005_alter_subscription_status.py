# Generated by Django 4.2.4 on 2023-10-09 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=10),
        ),
    ]