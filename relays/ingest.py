import logging
from typing import Union

import selfcord

from django.db import IntegrityError

from relays.models import (
    Channel, Message, MessageAttachment, MessageEmbed, Server, User,
)

logger = logging.getLogger(__name__)


def ingest_discord_message_new(message: selfcord.Message):
    try:
        logger.debug("DB Logging Message")
        new_message = Message.objects.create(
            message=message.id,
            content=f"{message.content}",
            channel_id=message.channel.id,
            user=User.objects.get_or_create(id=message.author.id, defaults={"name": message.author.display_name})[0],
            author_nick=message.author.display_name,
            timestamp=message.created_at,
            mention_everyone=message.mention_everyone)
        try:
            for e in message.embeds:
                MessageEmbed.objects.create(content=str(e.to_dict()), message=new_message)
        except Exception as e:
            logger.exception(e)
        try:
            for a in message.attachments:
                MessageAttachment.objects.create(id=a.id, url=a.url, filename=a.filename, message=new_message)
        except IntegrityError:
            pass
        except Exception as e:
            logger.exception(e)

    except IntegrityError:
        if isinstance(message.channel, selfcord.abc.GuildChannel):
            ingest_discord_guildchannel_new(message.channel)
        elif isinstance(message.channel, (selfcord.DMChannel, selfcord.GroupChannel)):
            ingest_discord_privatechannel_new(message.channel)
            return
        else:
            pass
    except Exception as e:
        logger.exception(e)


def ingest_discord_message_edit(before: selfcord.Message, after: selfcord.Message):
    if before.content == after.content and before.attachments == after.attachments and before.embeds == after.embeds:
        # The following non-exhaustive cases trigger this event:
        # A message has been pinned or unpinned.
        # The message content has been changed. <- We only care here.
        # The message has received an embed.
        # For performance reasons, the embed server does not do this in a “consistent” manner. <- this tends to result in non user-edit spam after a message is posted.
        # The message’s embeds were suppressed or unsuppressed.
        # A call message has received an update to its participants or ending time.
        return

    try:
        edit_count = Message.objects.filter(
            message=after.id).order_by("edit_count").last().edit_count
    except AttributeError:
        edit_count = 1
    except Exception as e:
        edit_count = 1
        logger.exception(e)
    try:
        new_message = Message.objects.create(
            message=after.id,
            content=f"{after.content}",
            channel_id=after.channel.id,
            user=User.objects.get_or_create(id=after.author.id, defaults={"name": after.author.display_name})[0],
            author_nick=after.author.display_name,
            timestamp=after.edited_at,
            mention_everyone=after.mention_everyone,
            edit_count=edit_count + 1)
        try:
            for e in after.embeds:
                MessageEmbed.objects.create(content=str(e.to_dict()), message=new_message)
        except Exception as e:
            logger.exception(e)
        try:
            for a in after.attachments:
                MessageAttachment.objects.create(id=a.id, url=a.url, filename=a.filename, message=new_message)
        except IntegrityError:
            pass
        except Exception as e:
            logger.exception(e)

    except IntegrityError:
        if isinstance(after.channel, selfcord.abc.GuildChannel):
            ingest_discord_guildchannel_new(after.channel)
        elif isinstance(after.channel, (selfcord.DMChannel, selfcord.GroupChannel)):
            ingest_discord_privatechannel_new(after.channel)
            return
        else:
            pass
    except Exception as e:
        logger.exception(e)


def ingest_discord_message_delete(message: selfcord.Message):
    try:
        # Call this once to trigger any signals
        final_message = Message.objects.filter(message=message.id).order_by("edit_count").last()
        if final_message is not None:
            final_message.deleted = True
            final_message.save()
    except Exception as e:
        logger.exception(e)

    try:
        # This is in bulk and wont trigger anything
        Message.objects.filter(message=message.id).update(deleted=True)
    except Exception as e:
        logger.exception(e)


def ingest_discord_guildchannel_new(channel: selfcord.abc.GuildChannel):
    try:
        if channel.category_id is not None:
            parent_excepted = Channel.objects.get(channel=channel.category_id)
        else:
            parent_excepted = None
    except Exception:
        # May already be None
        # May not be a valid attribute
        # May not be created yet
        parent_excepted = None

    try:
        if channel.type == selfcord.ChannelType.text:
            Channel.objects.create(
                channel=channel.id,
                name=channel.name,
                server_id=channel.guild.id,
                parent=parent_excepted,
                created_at=channel.created_at,
                channel_type=Channel.Channel_Type.TEXTCHANNEL)
        elif channel.type == selfcord.ChannelType.voice:
            Channel.objects.create(
                channel=channel.id,
                name=channel.name,
                server_id=channel.guild.id,
                parent=parent_excepted,
                created_at=channel.created_at,
                channel_type=Channel.Channel_Type.VOICECHANNEL)
        elif channel.type == selfcord.ChannelType.category:
            Channel.objects.create(
                channel=channel.id,
                name=channel.name,
                server_id=channel.guild.id,
                parent=parent_excepted,
                created_at=channel.created_at,
                channel_type=Channel.Channel_Type.CATEGORYCHANNEL)
        elif channel.type == selfcord.ChannelType.news:
            Channel.objects.create(
                channel=channel.id,
                name=channel.name,
                server_id=channel.guild.id,
                parent=parent_excepted,
                created_at=channel.created_at,
                channel_type=Channel.Channel_Type.TEXTCHANNEL)
        elif channel.type == selfcord.ChannelType.stage_voice:
            Channel.objects.create(
                channel=channel.id,
                name=channel.name,
                server_id=channel.guild.id,
                parent=parent_excepted,
                created_at=channel.created_at,
                channel_type=Channel.Channel_Type.STAGECHANNEL)
        elif channel.type == selfcord.ChannelType.news_thread:
            Channel.objects.create(
                channel=channel.id,
                name=channel.name,
                server_id=channel.guild.id,
                parent=parent_excepted,
                created_at=channel.created_at,
                channel_type=Channel.Channel_Type.THREAD)
        elif channel.type == selfcord.ChannelType.public_thread:
            Channel.objects.create(
                channel=channel.id,
                name=channel.name,
                server_id=channel.guild.id,
                parent=parent_excepted,
                created_at=channel.created_at,
                channel_type=Channel.Channel_Type.THREAD)
        elif channel.type == selfcord.ChannelType.private_thread:
            Channel.objects.create(
                channel=channel.id,
                name=channel.name,
                server_id=channel.guild.id,
                parent=parent_excepted,
                created_at=channel.created_at,
                channel_type=Channel.Channel_Type.THREAD)
        elif channel.type == selfcord.ChannelType.forum:
            Channel.objects.create(
                channel=channel.id,
                name=channel.name,
                server_id=channel.guild.id,
                parent=parent_excepted,
                created_at=channel.created_at,
                channel_type=Channel.Channel_Type.FORUMCHANNEL)
    except IntegrityError:
        pass  # this is fine
    except Exception as e:
        logger.exception(e)


def ingest_discord_privatechannel_new(channel: Union[selfcord.DMChannel, selfcord.GroupChannel]):

    if channel.type == selfcord.ChannelType.private:
        recipient = User.objects.get_or_create(id=channel.recipient.id, defaults={"name": channel.recipient.display_name})[0],
        c = Channel.objects.create(
            channel=channel.id,
            name="DMChannel",
            created_at=channel.created_at,
            channel_type=Channel.Channel_Type.DMCHANNEL)
        c.recipients.add(recipient)
        c.save
    elif channel.type == selfcord.ChannelType.group:
        recipients = []
        for recipient in channel.recipients:
            recipients.append(User.objects.get_or_create(id=recipient.id, defaults={"name": recipient.display_name})[0])
        c = Channel.objects.create(
            channel=channel.id,
            name="GroupChannel",
            created_at=channel.created_at,
            channel_type=Channel.Channel_Type.GROUPCHANNEL)
        c.recipients.add(recipients)
        c.save


def ingest_discord_guildchannel_edit(before: selfcord.abc.GuildChannel, after: selfcord.abc.GuildChannel):

    try:
        if after.category_id is not None:
            parent_excepted = Channel.objects.get(channel=after.category_id)
        else:
            parent_excepted = None
    except Exception:
        # May already be None
        # May not be a valid attribute
        # May not be created yet
        parent_excepted = None

    try:
        if after.type == selfcord.ChannelType.text:
            Channel.objects.update_or_create(
                channel=after.id,
                defaults={
                    "name": after.name,
                    "server_id": after.guild.id,
                    "parent": parent_excepted,
                    "created_at": after.created_at,
                    "channel_type": Channel.Channel_Type.TEXTCHANNEL})
        elif after.type == selfcord.ChannelType.voice:
            Channel.objects.update_or_create(
                channel=after.id,
                defaults={
                    "name": after.name,
                    "server_id": after.guild.id,
                    "parent": parent_excepted,
                    "created_at": after.created_at,
                    "channel_type": Channel.Channel_Type.VOICECHANNEL})
        elif after.type == selfcord.ChannelType.category:
            Channel.objects.update_or_create(
                channel=after.id,
                defaults={
                    "name": after.name,
                    "server_id": after.guild.id,
                    "parent": parent_excepted,
                    "created_at": after.created_at,
                    "channel_type": Channel.Channel_Type.CATEGORYCHANNEL})
        elif after.type == selfcord.ChannelType.news:
            Channel.objects.update_or_create(
                channel=after.id,
                defaults={
                    "name": after.name,
                    "server_id": after.guild.id,
                    "parent": parent_excepted,
                    "created_at": after.created_at,
                    "channel_type": Channel.Channel_Type.TEXTCHANNEL})
        elif after.type == selfcord.ChannelType.stage_voice:
            Channel.objects.update_or_create(
                channel=after.id,
                defaults={
                    "name": after.name,
                    "server_id": after.guild.id,
                    "parent": parent_excepted,
                    "created_at": after.created_at,
                    "channel_type": Channel.Channel_Type.STAGECHANNEL})
        elif after.type == selfcord.ChannelType.news_thread:
            Channel.objects.update_or_create(
                channel=after.id,
                defaults={
                    "name": after.name,
                    "server_id": after.guild.id,
                    "parent": parent_excepted,
                    "created_at": after.created_at,
                    "channel_type": Channel.Channel_Type.THREAD})
        elif after.type == selfcord.ChannelType.public_thread:
            Channel.objects.update_or_create(
                channel=after.id,
                defaults={
                    "name": after.name,
                    "server_id": after.guild.id,
                    "parent": parent_excepted,
                    "created_at": after.created_at,
                    "channel_type": Channel.Channel_Type.THREAD})
        elif after.type == selfcord.ChannelType.private_thread:
            Channel.objects.update_or_create(
                channel=after.id,
                defaults={
                    "name": after.name,
                    "server_id": after.guild.id,
                    "parent": parent_excepted,
                    "created_at": after.created_at,
                    "channel_type": Channel.Channel_Type.THREAD})
        elif after.type == selfcord.ChannelType.forum:
            Channel.objects.update_or_create(
                channel=after.id,
                defaults={
                    "name": after.name,
                    "server_id": after.guild.id,
                    "parent": parent_excepted,
                    "created_at": after.created_at,
                    "channel_type": Channel.Channel_Type.FORUMCHANNEL})
    except Exception as e:
        logger.exception(e)


def ingest_discord_privatechannel_edit(before: Union[selfcord.DMChannel, selfcord.GroupChannel], after: Union[selfcord.DMChannel, selfcord.GroupChannel]):
    if after.type == selfcord.ChannelType.private:
        Channel.objects.update_or_create(
            channel=after.id,
            defaults={
                "name": "DMChannel",
                "created_at": after.created_at,
                "channel_type": Channel.Channel_Type.DMCHANNEL,
            })
    elif after.type == selfcord.ChannelType.group:
        Channel.objects.update_or_create(
            channel=after.id,
            defaults={
                "name": "DMChannel",
                "created_at": after.created_at,
                "channel_type": Channel.Channel_Type.GROUPCHANNEL,
            })


def ingest_discord_channel_delete(channel: Union[selfcord.abc.PrivateChannel, selfcord.abc.GuildChannel]):
    try:
        deleted_channel = Channel.objects.get(channel=channel.id)
        deleted_channel.deleted = True
        deleted_channel.save()
    except Channel.DoesNotExist:
        # this is fine
        pass
    except Exception as e:
        logger.exception(e)


def ingest_discord_guild(guild: selfcord.Guild) -> Server:
    # No New/Edit, lightweight and rarely called so simplified into update_or_create
    try:
        server, created = Server.objects.update_or_create(
            server=guild.id,
            defaults={
                'name': guild.name,
                'protocol': Server.Protocol_Choice.DISCORD,
                "users": guild.member_count,
                "created_at": guild.created_at, })
    except Exception as e:
        logger.exception(e)
    return server
