# Generated by Django 4.1.6 on 2023-04-09 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='id',
            field=models.PositiveBigIntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]