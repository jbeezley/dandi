# Generated by Django 2.2.6 on 2019-10-26 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djaunty', '0003_auto_20191026_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='session_start_time',
            field=models.DateField(null=True),
        ),
    ]
