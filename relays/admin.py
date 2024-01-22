import logging

from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelectMultiple

from relays.models import (
    AccessToken, Channel, DestinationAADiscordBot, Event, Message,
    RelayConfiguration, RelaysConfig, Server, Webhook,
)

logger = logging.getLogger(__name__)


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ["name", "users", "protocol", "deleted", "server"]
    list_filter = ["protocol", "deleted"]
    ordering = ["-users", ]
    search_fields = ["name", "protocol"]


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ["token", "_server_list", "owner"]
    ordering = ["owner", ]
    list_filter = ['servers', 'owner', ]

    def _server_list(self, obj):
        return "\n".join([server.name for server in obj.servers.all()])


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'server',
                    "deleted", "channel_type", 'channel']
    ordering = ['name', ]
    list_filter = ['server', "channel_type", "deleted"]
    search_fields = ['name', 'parent', 'server', ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["message", "channel", "_servername",
                    "author_nick", "timestamp", "edit_count"]
    ordering = ['-timestamp',]
    list_filter = ["channel", "deleted"]
    search_fields = ["content", "channel", "server"]

    def _servername(self, obj):
        try:
            return obj.channel.server.name
        except Exception:
            return ""


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ["name", "url"]
    ordering = ["name", ]
    search_fields = ["name", ]


@admin.register(DestinationAADiscordBot)
class DestinationAADiscordBotAdmin(admin.ModelAdmin):
    list_display = ["destination", "destination"]
    ordering = ["destination", ]

    search_fields = ["destination", ]


class SourceChannelField(AutocompleteSelectMultiple):
    def label_from_instance(self, obj):
        return f"{obj} - {obj.server}"


@admin.register(RelayConfiguration)
class RelayConfigurationAdmin(admin.ModelAdmin):
    list_display = ["name", "message_mention", "message_non_mention",
                    "message_regex", "_source_server_list", "_source_channel_list", ]
    ordering = ["name", ]
    search_fields = ["name", ]

    filter_horizontal = [
        'source_servers', 'source_channels', 'destination_webhooks', 'destination_aadiscordbot']

    def _source_server_list(self, obj: RelayConfiguration):
        if obj.source_server_all is True:
            return "ALL"
        else:
            return "\n".join([source_server.name for source_server in obj.source_servers.all()])

    def _source_channel_list(self, obj: RelayConfiguration):
        if obj.source_channel_all is True:
            return "ALL"
        else:
            return "\n".join([source_channel.name for source_channel in obj.source_channels.all()])


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    ordering = ["start", ]
    search_fields = ["name", ]


@admin.register(RelaysConfig)
class RelaysConfigAdmin(admin.ModelAdmin):
    filter_horizontal = ["status_webhooks", ]
