import datetime
import logging

from discord import Colour, SyncWebhook
from solo.models import SingletonModel

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class Relays(models.Model):
    """Meta model for app permissions"""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('basic_access', 'Can access this app'),
        )


class Server(models.Model):
    """Servers and their ID"""

    class Protocol_Choice(models.TextChoices):
        DISCORD = 'Discord', _('Discord')
        SLACK = 'Slack', _('Slack')
        XMPP = 'XMPP', _('XMPP')

    server = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    protocol = models.CharField(max_length=10, default=Protocol_Choice.DISCORD,
                                choices=Protocol_Choice.choices)
    users = models.IntegerField(_("Users"), default=0)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Server'
        verbose_name_plural = 'Servers'

    def __str__(self):
        return f"{self.name}"

    def _last_message(self):
        return Message.objects.filter(
            channel__server=self.server).latest('timestamp')

    @property
    def last_message(self):
        return self._last_message()

    @property
    def last_message_oneday(self) -> bool:
        time_ref = timezone.now() - datetime.timedelta(days=1)

        if (self._last_message().timestamp < time_ref):
            return True
        else:
            return False

    @property
    def last_message_onehour(self) -> bool:
        time_ref = timezone.now() - datetime.timedelta(hours=1)

        if (self._last_message().timestamp < time_ref):
            return True
        else:
            return False

    @property
    def message_count(self):
        return Message.objects.filter(channel__server=self.server).count()


class User(models.Model):
    id = models.PositiveBigIntegerField(_("User ID"), primary_key=True)
    name = models.CharField(_("Username"), max_length=100, blank=True)
    bot = models.BooleanField(_("Is Bot User?"), default=False)
    created_at = models.DateTimeField(
        _("Created Timestamp"), auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        if self.bot is False:
            return f"{self.name}"
        else:
            return f"BOT: {self.name}"


class AccessToken(models.Model):
    """Access Token"""

    token = models.CharField(max_length=256)
    servers = models.ManyToManyField(Server, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, blank=True, null=True)

    appear_offline = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.token}"

    class Meta:
        verbose_name = 'Access Token'
        verbose_name_plural = 'Access Tokens'


class Channel(models.Model):
    """Channel IDs, Names and the Server they belong to"""
    class Channel_Type(models.TextChoices):
        # Thread
        THREAD = 'T', _('Thread')
        # GuildChannel
        TEXTCHANNEL = 'TC', _('GuildChannel.TextChannel')
        FORUMCHANNEL = 'FC', _('GuildChannel.ForumChannel')
        VOICECHANNEL = 'VC', _('GuildChannel.VoiceChannel')
        CATEGORYCHANNEL = 'CC', _('GuildChannel.ForumChannel')
        STAGECHANNEL = 'SC', _('GuildChannel.StageChannel')
        # PrivateChannel0
        DMCHANNEL = 'DM', _('PrivateChannel.DMChannel')
        GROUPCHANNEL = 'GM', _('PrivateChannel.GroupChannel')

    server = models.ForeignKey(Server, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, help_text="Channel in Category, Or Thread", related_name="channel_parent")
    recipients = models.ManyToManyField(User, verbose_name=_("Recipients"), blank=True)
    channel = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)
    channel_type = models.CharField(
        max_length=2, choices=Channel_Type.choices, default=Channel_Type.TEXTCHANNEL)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    @property
    def channel_as_path(self):
        if self.parent and self.parent.parent:
            return f"[{self.server}]/{self.parent.parent}/{self.parent}/{self}"
        elif self.parent:
            return f"{self.server}/{self.parent}/{self}"
        else:
            return f"{self.server}/{self}"

    @property
    def channel_as_path_noserver(self):
        if self.parent and self.parent.parent:
            return f"[{self.parent.parent}/{self.parent}/{self}"
        elif self.parent:
            return f"{self.parent}/{self}"
        else:
            return f"{self}"

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'
        indexes = [
            models.Index(fields=["server", "channel_type"]),
        ]


class Message(models.Model):
    """Message Storage"""
    message = models.PositiveBigIntegerField()
    edit_count = models.IntegerField(_("Edit Count"), default=1)

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    content = models.TextField(help_text="The primary content of a message")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    mention_everyone = models.BooleanField(_("Message is @everyone"), default=False)

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    author_nick = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'"{self.message}"'

    @property
    def server(self):
        return self.channel.server

    @property
    def content_extended(self) -> str:
        all_content = []
        try:
            for e in self.embeds.all():
                all_content.append(str(e.content))
        except Exception as e:
            logger.exception(e)
        try:
            for a in self.attachments.all():
                all_content.append(str(a.content))
        except Exception as e:
            logger.exception(e)
        content_extended = "\n".join(all_content)

        return content_extended

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        unique_together = ('message', 'edit_count')
        indexes = [
            models.Index(fields=["message", "channel", ]),
        ]


class MessageEmbed(models.Model):
    content = models.TextField(_("Message Embed to String"))
    message = models.ForeignKey(Message, verbose_name=_("Message"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("MessageEmbed")
        verbose_name_plural = _("MessageEmbeds")

    def __str__(self):
        return f'"{self.pk}"'


class MessageAttachment(models.Model):
    id = models.PositiveBigIntegerField(_("Attachment ID"), primary_key=True)
    filename = models.CharField(_("Filename"), max_length=256)
    media_type = models.CharField(_("Media Type"), max_length=50)
    url = models.CharField(_("URL"), max_length=2048)
    message = models.ForeignKey(Message, verbose_name=_("Message"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Message Attachment")
        verbose_name_plural = _("Message Attachments")

    def __str__(self):
        return f'{self.filename}'


class Webhook(models.Model):
    """Destinations for Relays"""
    url = models.CharField(max_length=2048)
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Destination Webhook'
        verbose_name_plural = 'Destination Webhooks'

    def send_embed(self, embed):
        webhook = SyncWebhook.from_url(self.url)
        webhook.send(embed=embed, username="AA Relays")


class DestinationAADiscordBot(models.Model):
    """Destination Channels to be passed to AA-Discord
    Bot DON'T set this to hostile channels you potato"""
    class Message_Type(models.TextChoices):
        CHANNEL_MESSAGE = 'CM', _('Channel Message')
        DIRECT_MESSAGE = 'DM', _('Direct Message')

    destination_type = models.CharField(max_length=2,
                                        choices=Message_Type.choices,
                                        default=Message_Type.CHANNEL_MESSAGE)
    destination = models.ForeignKey("aadiscordbot.channels", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.destination}"

    class Meta:
        verbose_name = 'Discord Channel Destination'
        verbose_name_plural = 'Discord Channel Destinations'


class RelayConfiguration(models.Model):
    """In and Out...... Repeat"""
    name = models.CharField(max_length=100)

    source_servers = models.ManyToManyField(Server, blank=True)
    source_server_all = models.BooleanField(default=False)
    source_channels = models.ManyToManyField(Channel, blank=True)
    source_channel_all = models.BooleanField(default=False)

    message_mention = models.BooleanField(default=True)
    message_non_mention = models.BooleanField(default=False)
    message_regex = models.CharField(max_length=10, default=".^", blank=False, null=False)

    relay_event = models.BooleanField(default=True)
    relay_embed = models.BooleanField(default=True)
    relay_private_message = models.BooleanField(default=True, help_text="Not Yet Implemented")

    destination_webhooks = models.ManyToManyField(Webhook, blank=True)
    destination_aadiscordbot = models.ManyToManyField(DestinationAADiscordBot, blank=True)

    attempt_translation = models.BooleanField(default=False)

    class Colours(models.TextChoices):
        BLUE = Colour.blue(), _('Blue')
        BLURPLE = Colour.blurple(), _('blurple')
        BRAND_GREEN = Colour.brand_green(), _('brand_green')
        BRAND_RED = Colour.brand_red(), _('brand_red')
        DARK_BLUE = Colour.dark_blue(), _('dark_blue')
        DARK_GOLD = Colour.dark_gold(), _('dark_gold')
        DARK_GREY = Colour.dark_grey(), _('dark_grey')
        DARK_GREEN = Colour.dark_green(), _('dark_green')
        DARK_MAGENTA = Colour.dark_magenta(), _('dark_magenta')
        DARK_ORANGE = Colour.dark_orange(), _('dark_orange')
        DARK_PURPLE = Colour.dark_purple(), _('dark_purple')
        DARK_RED = Colour.dark_red(), _('dark_red')
        DARK_TEAL = Colour.dark_teal(), _('dark_teal')
        DARK_THEME = Colour.dark_theme(), _('dark_theme')
        DARKER_GREY = Colour.darker_grey(), _('darker_grey')
        EMBED_BACKGROUND = Colour.embed_background('dark'), _('embed_background')
        FUCHSIA = Colour.fuchsia(), _('fuchsia')
        GOLD = Colour.gold(), _('gold')
        GREEN = Colour.green(), _('green')
        GREYPLE = Colour.greyple(), _('greyple')
        LIGHT_GREY = Colour.light_grey(), _('light_grey')
        LIGHTER_GREY = Colour.lighter_grey(), _('lighter_grey')
        NITRO_PINK = Colour.nitro_pink(), _('nitro_pink')
        OG_BLURPLE = Colour.og_blurple(), _('og_blurple')
        ORANGE = Colour.orange(), _('orange')
        PURPLE = Colour.purple(), _('purple')
        RED = Colour.red(), _('red')
        TEAL = Colour.teal(), _('teal')
        YELLOW = Colour.yellow(), _('yellow')

    override_colour = models.CharField(_("Override Colour"), max_length=50, choices=Colours.choices, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Relay Configuration'
        verbose_name_plural = 'Relay Configurations'


class Event(models.Model):
    event = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))
    start = models.DateTimeField(auto_now=False, auto_now_add=False)
    end = models.DateTimeField(auto_now=False, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("ScheduledEvent")
        verbose_name_plural = _("ScheduledEvents")

    def __str__(self):
        return f"{self.name}"


class RelaysConfig(SingletonModel):
    status_webhooks = models.ManyToManyField(
        Webhook, verbose_name=_("Destination Webhook for Status Updates"))

    def __str__(self):
        return "AA Relays Settings"

    class Meta:
        """
        Meta definitions
        """
        default_permissions = ()
        verbose_name = "AA Relays Settings"
        verbose_name_plural = "AA Relays Settings"
