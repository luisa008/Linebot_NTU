# Generated by Django 4.0.4 on 2022-04-20 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ntubot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='section',
            field=models.PositiveIntegerField(),
        ),
    ]
