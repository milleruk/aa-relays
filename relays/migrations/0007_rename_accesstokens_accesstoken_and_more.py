# Generated by Django 4.0.10 on 2023-06-12 11:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('relays', '0006_remove_relayconfigurations_token_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccessTokens',
            new_name='AccessToken',
        ),
        migrations.RenameModel(
            old_name='Channels',
            new_name='Channel',
        ),
        migrations.RenameModel(
            old_name='DestinationWebhooks',
            new_name='DestinationWebhook',
        ),
        migrations.RenameModel(
            old_name='Messages',
            new_name='Message',
        ),
        migrations.RenameModel(
            old_name='RelayConfigurations',
            new_name='RelayConfiguration',
        ),
        migrations.RenameModel(
            old_name='Servers',
            new_name='Server',
        ),
    ]
