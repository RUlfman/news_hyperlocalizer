# Generated by Django 5.0.4 on 2024-05-04 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('type', models.CharField(choices=[('LOCATION', 'Location'), ('CONTENT', 'Content'), ('CATEGORY', 'Category')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StoryLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.label')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.story')),
            ],
            options={
                'unique_together': {('story', 'label')},
            },
        ),
        migrations.AddField(
            model_name='story',
            name='labels',
            field=models.ManyToManyField(through='stories.StoryLabel', to='stories.label'),
        ),
    ]
