# Generated by Django 3.2.8 on 2021-12-17 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chessManagement', '0016_stage_tournament_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.TextField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
