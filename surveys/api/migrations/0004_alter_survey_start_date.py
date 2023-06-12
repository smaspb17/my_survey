# Generated by Django 4.2.2 on 2023-06-08 17:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_survey_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='start_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата старта - сегодня'),
        ),
    ]
