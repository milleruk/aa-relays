# Generated by Django 4.0.10 on 2023-06-13 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relays', '0017_alter_channel_recipients_alter_channel_server'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relaysconfig',
            old_name='status_webhook',
            new_name='status_webhooks',
        ),
    ]