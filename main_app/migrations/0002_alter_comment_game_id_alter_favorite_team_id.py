# Generated by Django 4.1.4 on 2023-01-05 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='game_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='team_id',
            field=models.IntegerField(),
        ),
    ]
