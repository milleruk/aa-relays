# Generated by Django 4.0.10 on 2023-06-19 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relays', '0010_remove_message_content_extended_messageembed_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relayconfiguration',
            old_name='event',
            new_name='relay_event',
        ),
        migrations.RenameField(
            model_name='relayconfiguration',
            old_name='private_message',
            new_name='relay_private_message',
        ),
        migrations.AddField(
            model_name='relayconfiguration',
            name='relay_embed',
            field=models.BooleanField(default=True),
        ),
    ]
