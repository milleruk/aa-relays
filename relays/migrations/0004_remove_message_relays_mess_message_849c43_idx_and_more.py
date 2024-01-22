# Generated by Django 4.0.10 on 2023-06-16 04:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relays', '0003_populate_user_model'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='message',
            name='relays_mess_message_849c43_idx',
        ),
        migrations.RenameField(
            model_name='relayconfiguration',
            old_name='destination_webhook',
            new_name='destination_webhooks',
        ),
        migrations.RenameField(
            model_name='relayconfiguration',
            old_name='source_channel',
            new_name='source_channels',
        ),
        migrations.RenameField(
            model_name='relayconfiguration',
            old_name='source_server',
            new_name='source_servers',
        ),
        migrations.AddField(
            model_name='relayconfiguration',
            name='event',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='relayconfiguration',
            name='override_colour',
            field=models.CharField(blank=True, choices=[('#3498db', 'Blue'), ('#5865f2', 'blurple'), ('#57f287', 'brand_green'), ('#ed4245', 'brand_red'), ('#206694', 'dark_blue'), ('#c27c0e', 'dark_gold'), ('#607d8b', 'dark_grey'), ('#1f8b4c', 'dark_green'), ('#ad1457', 'dark_magenta'), ('#a84300', 'dark_orange'), ('#71368a', 'dark_purple'), ('#992d22', 'dark_red'), ('#11806a', 'dark_teal'), ('#36393f', 'dark_theme'), ('#546e7a', 'darker_grey'), ('#2b2d31', 'embed_background'), ('#eb459e', 'fuchsia'), ('#f1c40f', 'gold'), ('#2ecc71', 'green'), ('#99aab5', 'greyple'), ('#979c9f', 'light_grey'), ('#95a5a6', 'lighter_grey'), ('#f47fff', 'nitro_pink'), ('#7289da', 'og_blurple'), ('#e67e22', 'orange'), ('#9b59b6', 'purple'), ('#e74c3c', 'red'), ('#1abc9c', 'teal'), ('#fee75c', 'yellow')], max_length=50, verbose_name=''),
        ),
        migrations.AddField(
            model_name='relayconfiguration',
            name='private_message',
            field=models.BooleanField(default=True, help_text='Not Yet Implemented'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='Channel in Category, Or Thread', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='channel_parent', to='relays.channel'),
        ),
    ]
