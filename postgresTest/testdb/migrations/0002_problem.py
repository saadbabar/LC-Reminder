# Generated by Django 4.2.13 on 2024-05-15 18:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_name', models.TextField()),
                ('difficulty', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='testdb.user')),
            ],
        ),
    ]