# Generated by Django 4.2.5 on 2023-10-11 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_card_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.ImageField(blank=True, upload_to='uploads/images/'),
        ),
    ]
