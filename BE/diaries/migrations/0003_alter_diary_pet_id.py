# Generated by Django 5.0.7 on 2024-07-26 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaries', '0002_alter_diary_content'),
        ('pets', '0004_rename_photo_pet_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='pet_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diaries', to='pets.pet'),
        ),
    ]
