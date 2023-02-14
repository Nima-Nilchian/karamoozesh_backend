# Generated by Django 3.2 on 2023-02-13 21:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='the phone number is wrong!', regex='^(09|\\+989)\\d{9}$')]),
        ),
    ]