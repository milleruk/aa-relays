import argparse
import logging
import os
from datetime import datetime
from typing import Union

import selfcord

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myauth.settings.local")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from relays.helpers import (  # noqa:E402
    embed_status_disconnect, embed_status_kicked, embed_status_resumed,
    embed_status_started,
)
from relays.ingest import (  # noqa:E402
    ingest_discord_channel_delete, ingest_discord_guild,
    ingest_discord_guildchannel_edit, ingest_discord_guildchannel_new,
    ingest_discord_message_delete, ingest_discord_message_edit,
    ingest_discord_message_new, ingest_discord_privatechannel_edit,
    ingest_discord_privatechannel_new,
)
from relays.models import (  # noqa:E402
    AccessToken, Channel, Event, RelaysConfig,
)

parser = argparse.ArgumentParser()
parser.add_argument("runnertokenid")
args = parser.parse_args()

logger = logging.getLogger(__name__)


runnertoken = AccessToken.objects.get(id=args.runnertokenid)
client = selfcord.Client()

logger.debug(
    f"AA Relays config #{args.runnertokenid} Started at: {datetime.utcnow().strftime('%B %d %H:%M')}")


def now():
    return datetime.utcnow().strftime('%B %d %H:%M')


@client.event
async def on_ready():
    logger.debug(f"AA Relays config #{runnertoken.pk} at: {now()}")
    # Set Offline if wanted
    if runnertoken.appear_offline:
        await client.change_presence(status=selfcord.Status.offline, afk=True)
    # Populate Models on opening the client
    for guild in list(client.guilds):
        server = ingest_discord_guild(guild)
        runnertoken.servers.add(server)
        for channel in list(guild.channels):
            # new wont capture offline edits, but this is just bulk model making
            ingest_discord_guildchannel_new(channel)
    runnertoken.save()
    try:
        for webhook in RelaysConfig.get_solo().status_webhooks.all():
            webhook.send_embed(embed_status_started(runnertoken))
    except Exception as e:
        logger.exception(e)
        pass


@client.event
async def on_message(message: selfcord.Message):
    logger.debug("on_message() Called")
    ingest_discord_message_new(message)


@client.event
async def on_message_edit(before: selfcord.Message, after: selfcord.Message):
    logger.debug("on_message_edit() Called")
    ingest_discord_message_edit(before, after)


@client.event
async def on_message_delete(message: selfcord.Message):
    logger.debug("on_message_delete() Called")
    ingest_discord_message_delete(message)


@client.event
async def on_guild_channel_delete(channel: selfcord.abc.GuildChannel):
    logger.debug("on_message_delete() Called")
    ingest_discord_channel_delete(channel)


@client.event
async def on_guild_channel_create(channel: selfcord.abc.GuildChannel):
    logger.debug("on_message_delete() Called")
    ingest_discord_guildchannel_new(channel)


@client.event
async def on_guild_channel_update(before: selfcord.abc.GuildChannel, after: selfcord.abc.GuildChannel):
    logger.debug("on_guild_channel_update() Called")
    ingest_discord_guildchannel_edit(before, after)


@client.event
async def on_guild_update(before_guild: selfcord.Guild, after_guild: selfcord.Guild):
    logger.debug("on_guild_update() Called")
    ingest_discord_guild(after_guild)


async def on_guild_join(guild: selfcord.Guild):
    logger.debug("on_guild_join() Called")
    ingest_discord_guild(guild)
    for channel in list(guild.channels):
        ingest_discord_guildchannel_new(channel)


async def on_guild_remove(guild: selfcord.Guild):
    logger.debug("on_guild_remove() Called")
    try:
        for webhook in RelaysConfig.get_solo().status_webhooks.all():
            webhook.send_embed(embed_status_kicked(runnertoken, guild))
    except Exception as e:
        logger.exception(e)
        pass


async def on_scheduled_event_create(event: selfcord.ScheduledEvent):
    logger.debug("on_scheduled_event_create() Called")
    try:
        Event.objects.create(
            event=event.id,
            name=event.name,
            description=event.description,
            start_time=event.start_time,
            end_time=event.end_time
        )
    except Exception as e:
        logger.exception(e)


async def on_scheduled_event_delete(event: selfcord.ScheduledEvent):
    logger.debug("on_scheduled_event_delete() Called")
    try:
        deleted_event = Event.objects.get(event=event.id)
        deleted_event.deleted = True
        deleted_event.save()
    except Event.DoesNotExist:
        # this is fine
        pass
    except Exception as e:
        logger.exception(e)


async def on_thread_create(thread: selfcord.Thread):
    logger.debug("on_thread_create() Called")
    try:
        Channel.objects.create(
            channel=thread.id,
            parent=thread.parent_id,
            name=thread.name,
            server_id=thread.guild.id,
            channel_type=Channel.Channel_Type.THREAD)
    except Exception as e:
        logger.exception(e)


async def on_thread_delete(thread: selfcord.Thread):
    logger.debug("on_thread_delete() Called")
    try:
        deleted_thread = Channel.objects.get(channel=thread.id)
        deleted_thread.deleted = True
        deleted_thread.save()
    except Channel.DoesNotExist:
        # this is fine
        pass
    except Exception as e:
        logger.exception(e)


async def on_private_channel_create(channel: Union[selfcord.DMChannel, selfcord.GroupChannel]):
    ingest_discord_privatechannel_new(channel)


async def on_private_channel_update(before: Union[selfcord.DMChannel, selfcord.GroupChannel], after: Union[selfcord.DMChannel, selfcord.GroupChannel]):
    ingest_discord_privatechannel_edit(before, after)


async def on_private_channel_delete(channel):
    ingest_discord_channel_delete(channel)


client.run(token=runnertoken.token)
