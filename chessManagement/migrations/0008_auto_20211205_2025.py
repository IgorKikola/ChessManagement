# Generated by Django 3.2.8 on 2021-12-05 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chessManagement', '0007_game_tournament_userintournament'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='end_date',
            new_name='deadline',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='start_date',
        ),
    ]
