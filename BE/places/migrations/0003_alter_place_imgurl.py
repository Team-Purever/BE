# Generated by Django 5.0.7 on 2024-07-30 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_alter_place_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='imgUrl',
            field=models.ImageField(upload_to='place_photos'),
        ),
    ]
