# Generated by Django 4.2.3 on 2023-07-31 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StPage', '0003_stinfomodels_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='stinfomodels',
            name='Pass',
            field=models.BooleanField(null=True),
        ),
    ]
