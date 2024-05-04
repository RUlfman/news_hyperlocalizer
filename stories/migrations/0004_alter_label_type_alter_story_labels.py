# Generated by Django 5.0.4 on 2024-05-04 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_alter_label_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='type',
            field=models.CharField(choices=[('LOCATION', 'Locatie'), ('TOPIC', 'Onderwerp'), ('CATEGORY', 'Categorie'), ('AUDIENCE', 'Doelgroep')], max_length=20),
        ),
        migrations.AlterField(
            model_name='story',
            name='labels',
            field=models.ManyToManyField(blank=True, through='stories.StoryLabel', to='stories.label'),
        ),
    ]
