# Generated by Django 4.1.6 on 2023-04-09 15:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_alter_wallet_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='book_balance',
        ),
        migrations.AddField(
            model_name='history',
            name='action',
            field=models.CharField(choices=[('transfer', 'Transfer'), ('fund', 'Fund')], default='fund', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]