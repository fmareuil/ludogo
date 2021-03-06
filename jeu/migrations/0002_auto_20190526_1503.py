# Generated by Django 2.2.1 on 2019-05-26 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='agemin',
            field=models.IntegerField(help_text='age minimum', null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='tarif',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='timemax',
            field=models.IntegerField(help_text='temps de jeu maximum', null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='timemin',
            field=models.IntegerField(help_text='temps de jeu minimum', null=True),
        ),
    ]
