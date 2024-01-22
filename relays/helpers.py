import ast
import difflib
import logging
from datetime import datetime
from typing import Union

from aadiscordbot.app_settings import get_site_url
from discord import Colour, Embed
from googletrans import Translator
from selfcord import Guild as SelfcordGuild

from relays import __version__
from relays.app_settings import RELAYS_APP_BRANDNAME
from relays.models import AccessToken, Message, MessageEmbed

logger = logging.getLogger(__name__)

translator = Translator()


def embed_status_started(runnertoken: AccessToken) -> Embed:
    embed = Embed()
    embed.title = f"{RELAYS_APP_BRANDNAME}: Started"
    embed.colour = Colour.green()
    embed.description = f"**Runner {runnertoken.pk}**"
    for server in runnertoken.servers.all():
        embed.description += f"\n{server}"
    embed.url = "https://gitlab.com/tactical-supremacy/aa-drifters"
    embed.set_thumbnail(url="https://images.evetech.net/types/34495/render?size=128")
    embed.set_footer(
        text=f"VOLTA Relays v{__version__}")
    embed.timestamp = datetime.now()
    return embed


def embed_status_resumed(runnertoken: AccessToken) -> Embed:
    embed = Embed()
    embed.title = f"{RELAYS_APP_BRANDNAME}: Resumed"
    embed.color = Colour.yellow()
    embed.description = f"**Runner {runnertoken.pk}**"
    for server in runnertoken.servers.all():
        embed.description += f"\n{server}"
    embed.url = "https://gitlab.com/tactical-supremacy/aa-drifters"
    embed.set_thumbnail(url="https://images.evetech.net/types/34495/render?size=128")
    embed.set_footer(
        text=f"VOLTA Relays v{__version__}")
    embed.timestamp = datetime.now()
    return embed


def embed_status_disconnect(runnertoken: AccessToken) -> Embed:
    embed = Embed()
    embed.title = f"{RELAYS_APP_BRANDNAME}: Disconnected"
    embed.color = Colour.red()
    embed.description = f"**Runner {runnertoken.pk}**"
    for server in runnertoken.servers.all():
        embed.description += f"\n{server}"
    embed.url = "https://gitlab.com/tactical-supremacy/aa-drifters"
    embed.set_thumbnail(url="https://images.evetech.net/types/34495/render?size=128")
    embed.set_footer(
        text=f"VOLTA Relays v{__version__}")
    embed.timestamp = datetime.now()
    return embed


def embed_status_kicked(runnertoken: AccessToken, guild: SelfcordGuild) -> Embed:
    embed = Embed()
    embed.title = f"{RELAYS_APP_BRANDNAME}: Kicked from Server"
    embed.color = Colour.red()
    embed.description = f"Runner {runnertoken.pk}Server: {guild}"
    embed.url = "https://gitlab.com/tactical-supremacy/aa-drifters"
    embed.set_thumbnail(url="https://images.evetech.net/types/34495/render?size=128")
    embed.set_footer(
        text=f"VOLTA Relays v{__version__}")
    embed.timestamp = datetime.now()
    return embed


def embed_relay_guildmessage(message: Message, attempt_translation: bool, override_colour: Union[None, str] = None):
    embed = Embed()
    embed.url = f"{get_site_url()}/relays/server/{message.channel.server.server}"
    embed.timestamp = message.timestamp

    if message.edit_count == 1:
        embed.title = f"{RELAYS_APP_BRANDNAME}: [{message.channel.server}]"
        embed.description = f'''
            {message.channel.parent}/**{message.channel}**
            {message.user} aka **{message.author_nick}**
            EVE Time: {message.timestamp}
            '''
        if message.content:
            embed.description += f"```\n{message.content}\n```"
    else:
        embed.title = f"{RELAYS_APP_BRANDNAME}: [{message.channel.server}] - EDIT"
        before_message = Message.objects.get(
            message=message.message, edit_count=(message.edit_count - 1))
        embed.description = f"{message.channel.parent}/**{message.channel}**/{message.user} aka **{message.author_nick}**```\n" + '\n'.join(
            difflib.unified_diff(
                before_message.content.split("\n"),
                message.content.split("\n"),
                fromfile=f"{before_message.timestamp}",
                tofile=f"{message.timestamp}",
                n=0,  # no context strings wanted
                lineterm=""  # we already join \n, this is to stop it adding its own
            )) + "\n```"

    if attempt_translation is True:
        try:
            embed.description += f"Translated Content:\n```\n{translator.translate(text=message.content).text}```"
        except Exception as e:
            logger.exception(e)
    else:
        pass

    if override_colour is not None:
        embed.colour = Colour(value=int(override_colour))
    elif message.mention_everyone is True:
        embed.colour = Colour.red()
    else:
        pass

    embed.set_footer(
        icon_url="https://images.evetech.net/types/34495/render?size=128",
        text=f"VOLTA Relays v{__version__}"
    )
    return embed


def embed_relay_privatemessage(message: Message, attempt_translation: bool, override_colour: Union[None, str] = None):
    embed = Embed()
    embed.url = f"{get_site_url()}/relays/channel/{message.channel.channel}"
    embed.timestamp = message.timestamp

    if message.edit_count == 1:
        embed.title = f"{RELAYS_APP_BRANDNAME}: DM [{message.channel}]"
        embed.description = f'''
            {message.channel.parent}/**{message.channel}**
            {message.user} aka **{message.author_nick}**
            EVE Time: {message.timestamp}
            '''
        if message.content:
            embed.description += f"```\n{message.content}\n```"
    else:
        embed.title = f"{RELAYS_APP_BRANDNAME}: DM [{message.channel}]"
        before_message = Message.objects.get(
            message=message.message, edit_count=(message.edit_count - 1))
        embed.description = f"{message.channel.parent}/**{message.channel}**/{message.user} aka **{message.author_nick}**```\n" + '\n'.join(
            difflib.unified_diff(
                before_message.content.split("\n"),
                message.content.split("\n"),
                fromfile=f"{before_message.timestamp}",
                tofile=f"{message.timestamp}",
                n=0,  # no context strings wanted
                lineterm=""  # we already join \n, this is to stop it adding its own
            )) + "\n```"

    if attempt_translation is True:
        try:
            embed.description += f"Translated Content:\n```\n{translator.translate(text=message.content).text}```"
        except Exception as e:
            logger.exception(e)
    else:
        pass

    if override_colour is not None:
        embed.colour = Colour(value=int(override_colour))
    elif message.mention_everyone is True:
        embed.colour = Colour.red()
    else:
        pass

    embed.set_footer(
        icon_url="https://images.evetech.net/types/34495/render?size=128",
        text=f"VOLTA Relays v{__version__}"
    )
    return embed


def embed_relay_embed(messageembed: MessageEmbed, message: Message, attempt_translation: bool, override_colour: Union[None, str] = None):
    embed = Embed()
    embed.title = f"{RELAYS_APP_BRANDNAME}: [{message.channel.server}] - Embed"
    embed.url = f"{get_site_url()}/relays/server/{message.channel.server.server}"
    embed.timestamp = message.timestamp

    embed.description = f'''
        {message.channel.parent}/**{message.channel}**
        {message.user} aka **{message.author_nick}**
        EVE Time: {message.timestamp}
        '''
    has_content = False
    try:
        e = Embed.from_dict(ast.literal_eval(messageembed.content))
        if str(e.description) != "Embed.Empty":  # This proxy doesnt seem to trigger the error unless we stringcast it
            embed.description += f"\nEmbed:\n{e.description}"
            has_content = True
        if e.image.url != Embed.Empty:
            embed.description += f"\nImage:\n{e.image.url}"
            has_content = True
        if e.video.url != Embed.Empty:
            embed.description += f"\nVideo:\n{e.video.url}"
            has_content = True
        for y in e.fields:
            embed.add_field(name=y.name, value=y.value)
            # i hate this, so much
            has_content = True
    except Exception as e:
        logger.exception(e)

    if override_colour is not None:
        embed.colour = Colour(value=int(override_colour))
    elif message.mention_everyone is True:
        embed.colour = Colour.red()
    else:
        pass

    embed.set_footer(
        icon_url="https://images.evetech.net/types/34495/render?size=128",
        text=f"VOLTA Relays v{__version__}"
    )
    if has_content:
        return embed
    else:
        pass
