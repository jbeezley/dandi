# Generated by Django 2.2.6 on 2019-10-28 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djaunty', '0004_auto_20191026_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='age_in_days',
        ),
        migrations.AddField(
            model_name='dataset',
            name='age',
            field=models.DurationField(null=True),
        ),
    ]
