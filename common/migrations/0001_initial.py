# Generated by Django 2.2.1 on 2019-05-24 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(help_text='Prenom', max_length=100)),
                ('lastname', models.CharField(help_text='Nom de Famille', max_length=100)),
            ],
            options={
                'unique_together': {('firstname', 'lastname')},
            },
        ),
        migrations.CreateModel(
            name='Localisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nom du lieu', max_length=100)),
                ('details', models.CharField(help_text="details de l'emplacement", max_length=100)),
            ],
            options={
                'unique_together': {('name', 'details')},
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nom du genre', max_length=100)),
                ('type', models.CharField(choices=[('film', 'film'), ('jeu', 'jeu')], help_text='Type du genre', max_length=100)),
                ('description', models.CharField(blank=True, help_text='Une courte description du genre', max_length=150)),
            ],
            options={
                'unique_together': {('name', 'type')},
            },
        ),
    ]
