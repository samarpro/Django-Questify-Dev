# Generated by Django 4.2.3 on 2023-07-29 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StPage', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stinfomodels',
            name='Grade',
            field=models.IntegerField(default=0),
        ),
    ]
