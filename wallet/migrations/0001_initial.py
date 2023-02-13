# Generated by Django 4.1.6 on 2023-02-09 23:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('amount', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('book_balance', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]