# Generated by Django 5.0.7 on 2024-07-24 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='content',
            field=models.TextField(),
        ),
    ]
