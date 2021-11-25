# Generated by Django 3.2.8 on 2021-11-23 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chessManagement', '0003_user_user_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=520)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_level',
        ),
        migrations.CreateModel(
            name='UserInClub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_level', models.IntegerField(choices=[(0, 'Applicant'), (1, 'Member'), (2, 'Officer'), (3, 'Owner')], default=0)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chessManagement.club')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='userinclub',
            constraint=models.UniqueConstraint(fields=('user', 'club'), name='unique_user_in_club'),
        ),
    ]