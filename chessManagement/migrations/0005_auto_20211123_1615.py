# Generated by Django 3.2.8 on 2021-11-23 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chessManagement', '0004_auto_20211123_1559'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userinclub',
            name='unique_user_in_club',
        ),
        migrations.RemoveField(
            model_name='club',
            name='id',
        ),
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='userinclub',
            unique_together={('user', 'club')},
        ),
        migrations.RemoveField(
            model_name='userinclub',
            name='user_level',
        ),
    ]
