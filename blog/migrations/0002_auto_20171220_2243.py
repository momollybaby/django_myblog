# Generated by Django 2.0 on 2017-12-20 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(error_messages={'unique': 'A user with that phone number already exists.'}, unique=True, verbose_name='phone number'),
        ),
    ]
