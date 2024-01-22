import logging

from discord import AutocompleteContext, Option
from discord.commands import SlashCommandGroup
from discord.embeds import Embed
from discord.ext import commands

from django.conf import settings

from relays import __version__
from relays.models import AccessToken, Server

logger = logging.getLogger(__name__)


class Relays(commands.Cog):
    """
    AA-Relays Status and management slash commands
    """

    def __init__(self, bot):
        self.bot = bot

    relay_commands = SlashCommandGroup(
        "relays", "Relays", guild_ids=[int(settings.DISCORD_GUILD_ID)])

    async def search_servers(self, ctx: AutocompleteContext):
        """
        Returns a list of Servers that begin with the characters entered so far

        :param ctx: _description_
        :type ctx: Servers
        :return: _description_
        :rtype: list
        """
        return list(Server.objects.filter(name__icontains=ctx.value).values_list('name', 'server')[:10])

    @relay_commands.command(name="about", description="About the Discord Bot", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def about(self, ctx):
        """
        All about the bot
        """
        embed = Embed(title="AA Relays")
        embed.description = "What did you have for breakfast !?!"
        embed.url = "https://gitlab.com/tactical-supremacy/aa-relays"
        embed.set_thumbnail(url="https://images.evetech.net/types/11578/icon?size=64")
        embed.set_footer(
            text="Developed to enable TIKLE to fight above its weight class, now you can too")
        embed.add_field(
            name="Version", value=f"{__version__}", inline=False
        )

        return await ctx.respond(embed=embed)

    @relay_commands.command(name="add_token", description="About the Discord Bot", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def add_token(
        self, ctx,
        token_string=Option(str, "Discord Token"),
        appear_offline=Option(bool, "Appear Offline?", default='True', choices=["True", "False"])
    ):
        """
        Add a Discord Token to AA-Relays

        :param ctx: _description_
        :type ctx: _type_
        :param token_string: _description_, defaults to Option(str, "Discord Token")
        :type token_string: _type_, optional
        :param appear_offline: _description_, defaults to Option(bool, "Appear Offline?", default='True', choices=["True", "False"])
        :type appear_offline: _type_, optional
        """
        await ctx.trigger_typing()

        try:
            AccessToken.objects.get_or_create(token=token_string, appear_offline=appear_offline)
        except Exception as e:
            logger.exception(e)

        return await ctx.respond("Done")

    @relay_commands.command(name="status_server", description="Status of a Relayed Server", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def status_server(
            self, ctx,
            server=Option(int, "Server", autocomplete=search_servers),):
        """
        All about the bot
        """
        server_obj = Server.objects.get(id=server)
        return await ctx.respond(server_obj.last_message)


def setup(bot):
    bot.add_cog(Relays(bot))
