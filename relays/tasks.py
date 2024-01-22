import logging
import re

from celery import shared_task

from relays.app_settings import aadiscordbot_active
from relays.helpers import (
    embed_relay_embed, embed_relay_guildmessage, embed_relay_privatemessage,
)
from relays.models import (
    Channel, DestinationAADiscordBot, Message, MessageEmbed,
    RelayConfiguration,
)

if aadiscordbot_active():
    from aadiscordbot.tasks import send_message
logger = logging.getLogger(__name__)


@shared_task
def process_message(message_pk: int):
    # called by the signal of a new message being created.
    message = Message.objects.get(pk=message_pk)
    if message.content == "":
        # This will be handled by other process_message tasks
        return
    for relayconfiguration in RelayConfiguration.objects.all():
        if message.channel.channel_type in (Channel.Channel_Type.DMCHANNEL, Channel.Channel_Type.GROUPCHANNEL) and relayconfiguration.relay_private_message is True:
            if relayconfiguration.destination_webhooks.all() is not None:
                try:
                    for webhook in relayconfiguration.destination_webhooks.all():
                        webhook.send_embed(embed_relay_privatemessage(
                            message, attempt_translation=relayconfiguration.attempt_translation))
                except Exception as e:
                    logger.exception(e)
            if relayconfiguration.destination_aadiscordbot.all() is not None and aadiscordbot_active():
                try:
                    for destination in relayconfiguration.destination_aadiscordbot.all():
                        if destination.destination_type == DestinationAADiscordBot.Message_Type.DIRECT_MESSAGE:
                            raise NotImplementedError
                        elif destination.destination_type == DestinationAADiscordBot.Message_Type.CHANNEL_MESSAGE:
                            send_message(
                                channel_id=destination.destination.channel,
                                embed=(embed_relay_privatemessage(message, attempt_translation=relayconfiguration.attempt_translation)))
                        else:
                            pass
                except Exception as e:
                    logger.exception(e)
        else:
            if relayconfiguration.source_servers.filter(server=message.channel.server.server) or relayconfiguration.source_server_all is True:
                if relayconfiguration.source_channels.filter(channel=message.channel.channel) or relayconfiguration.source_channel_all is True:
                    try:
                        joined_content_with_headers = f"{message.channel.server.name}/{message.channel.name}/{message.author_nick}: {message.content}"
                    except Exception:
                        joined_content_with_headers = message.content
                    if message.mention_everyone == relayconfiguration.message_mention \
                            or message.mention_everyone != relayconfiguration.message_non_mention \
                            or re.search(relayconfiguration.message_regex, joined_content_with_headers) is not None:

                        if relayconfiguration.destination_webhooks.all() is not None:
                            try:
                                for webhook in relayconfiguration.destination_webhooks.all():
                                    webhook.send_embed(embed_relay_guildmessage(
                                        message, attempt_translation=relayconfiguration.attempt_translation))
                            except Exception as e:
                                logger.exception(e)

                        if relayconfiguration.destination_aadiscordbot.all() is not None and aadiscordbot_active():
                            # AA Discordbot uses its own Queue
                            try:
                                for destination in relayconfiguration.destination_aadiscordbot.all():
                                    if destination.destination_type == 'DM':
                                        raise NotImplementedError
                                    elif destination.destination_type == 'CM':
                                        send_message(
                                            channel_id=destination.destination.channel,
                                            embed=(embed_relay_guildmessage(message, attempt_translation=relayconfiguration.attempt_translation)))
                                    else:
                                        pass
                            except Exception as e:
                                logger.exception(e)


@shared_task
def process_embed(embed_pk: int):
    # called by the signal of a new embed being created
    messageembed = MessageEmbed.objects.get(pk=embed_pk)
    message = messageembed.message
    for relayconfiguration in RelayConfiguration.objects.all():
        if relayconfiguration.relay_embed is not True:
            continue
        if relayconfiguration.source_servers.filter(server=message.channel.server.server) or relayconfiguration.source_server_all is True:
            if relayconfiguration.source_channels.filter(channel=message.channel.channel) or relayconfiguration.source_channel_all is True:
                try:
                    joined_content_with_headers = f"{message.channel.server.name}/{message.channel.name}/{message.author_nick}: {message.content}"
                except Exception:
                    joined_content_with_headers = message.content

                if message.mention_everyone == relayconfiguration.message_mention \
                        or message.mention_everyone != relayconfiguration.message_non_mention \
                        or re.search(relayconfiguration.message_regex, joined_content_with_headers) is not None:

                    if relayconfiguration.destination_webhooks.all() is not None:
                        try:
                            for webhook in relayconfiguration.destination_webhooks.all():
                                webhook.send_embed(embed_relay_embed(
                                    messageembed=messageembed,
                                    message=message,
                                    attempt_translation=relayconfiguration.attempt_translation))
                        except Exception as e:
                            logger.exception(e)

                    if relayconfiguration.destination_aadiscordbot.all() is not None and aadiscordbot_active():
                        # AA Discordbot uses its own Queue
                        try:
                            for destination in relayconfiguration.destination_aadiscordbot.all():
                                if destination.destination_type == 'DM':
                                    raise NotImplementedError
                                elif destination.destination_type == 'CM':
                                    embed = (embed_relay_embed(
                                        messageembed=messageembed,
                                        message=message,
                                        attempt_translation=relayconfiguration.attempt_translation))
                                    if embed is not None:
                                        send_message(channel_id=destination.destination.channel, embed=embed)
                                else:
                                    pass
                        except Exception as e:
                            logger.exception(e)
