# Generated by Django 2.2.1 on 2019-05-29 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0007_auto_20190529_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='certificate',
            field=models.CharField(choices=[('Tous Publics', 'Tous Publics'), ('Tous Publics (avec avertissement)', 'Tous Publics (avec avertissement)'), ('10', 'plus de 10ans'), ('12', 'plus de 12ans'), ('16', 'plus de 16ans'), ('18', 'plus de 18ans'), ('X', 'Adult')], help_text='certification', max_length=50),
        ),
    ]
