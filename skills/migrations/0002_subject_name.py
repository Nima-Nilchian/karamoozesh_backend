# Generated by Django 3.2 on 2023-01-27 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='name',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
    ]
