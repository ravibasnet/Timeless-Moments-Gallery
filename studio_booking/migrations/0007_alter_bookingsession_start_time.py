# Generated by Django 5.2.1 on 2025-07-03 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio_booking', '0006_bookingsession_gallery_images_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingsession',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
