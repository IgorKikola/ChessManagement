# Generated by Django 3.2.8 on 2021-12-05 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chessManagement', '0008_auto_20211205_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='userintournament',
            name='is_co_organiser',
            field=models.BooleanField(default=False),
        ),
    ]
