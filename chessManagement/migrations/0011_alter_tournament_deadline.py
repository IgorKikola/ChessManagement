# Generated by Django 3.2.8 on 2021-12-09 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chessManagement', '0010_merge_20211208_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='deadline',
            field=models.DateField(null=True),
        ),
    ]
