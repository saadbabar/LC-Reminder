# Generated by Django 4.2.13 on 2024-05-24 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0005_problems_submissions_delete_problem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problems',
            name='EF',
            field=models.FloatField(default=2.5),
        ),
        migrations.AlterField(
            model_name='problems',
            name='interval',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='problems',
            name='repetitions',
            field=models.IntegerField(default=0),
        ),
    ]
