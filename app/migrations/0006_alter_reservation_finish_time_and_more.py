# Generated by Django 4.2.4 on 2024-03-25 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_reservation_finish_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='finish_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
