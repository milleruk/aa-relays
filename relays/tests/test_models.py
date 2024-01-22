from aadiscordbot.models import (
    Channels as AADiscordBotChannels, Servers as AADiscordBotServers,
)

from django.test import TestCase
from django.utils import timezone

from relays.models import (
    AccessToken, Channel, DestinationAADiscordBot, Event, Message,
    RelayConfiguration, Relays, RelaysConfig, Server, User, Webhook,
)


class ServerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, name="testuser")
        self.server = Server.objects.create(server=1, name="Test Server", protocol="Discord")
        self.channel = Channel.objects.create(channel=1, name="Test Channel", server=self.server)

    def test_server_last_message(self):
        message = Message.objects.create(
            message=1, channel=self.channel, content="Test message 1", user=self.user, timestamp=timezone.now())
        self.assertEqual(self.server.last_message, message)
        message2 = Message.objects.create(
            message=2, channel=self.channel, content="Test message 2", user=self.user, timestamp=timezone.now())
        self.assertEqual(self.server.last_message, message2)
        self.assertEqual(self.server.message_count, 2)
        self.assertFalse(self.server.last_message_oneday)
        self.assertFalse(self.server.last_message_onehour)


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, name="Test User")

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), "Test User")


class ChannelModelTest(TestCase):
    def setUp(self):
        self.server = Server.objects.create(server=1, name="Test Server", protocol="Discord")
        self.channel = Channel.objects.create(channel=1, name="Test Channel", server=self.server)

    def test_channel_str_representation(self):
        self.assertEqual(str(self.channel), "Test Channel")

    def test_channel_channel_as_path(self):
        self.assertEqual(self.channel.channel_as_path, "Test Server/Test Channel")
        parent_channel = Channel.objects.create(
            channel=2, server=self.server, name="Parent Channel", parent=None,)
        child_channel = Channel.objects.create(
            channel=3, server=self.server, name="Child Channel", parent=parent_channel,)
        self.assertEqual(child_channel.channel_as_path, "Test Server/Parent Channel/Child Channel")

    def test_channel_server(self):
        self.assertEqual(self.channel.server, self.server)


class MessageModelTest(TestCase):
    def setUp(self):
        self.server = Server.objects.create(server=1, name="Test Server", protocol="Discord")
        self.channel = Channel.objects.create(channel=1, name="Test Channel", server=self.server)
        self.user = User.objects.create(id=1, name="Test User")
        self.message = Message.objects.create(
            message=1, channel=self.channel, content="Test message", user=self.user)

    def test_message_server(self):
        self.assertEqual(self.message.server, self.server)

    def test_message_edit_count(self):
        self.assertEqual(self.message.edit_count, 1)

    def test_message_mentions(self):
        self.assertFalse(self.message.mention_everyone)

    def test_message_timestamp(self):
        self.assertIsNotNone(self.message.timestamp)


class RelaysModelTest(TestCase):
    def test_relay_basic_access_permission(self):
        self.assertEqual(Relays._meta.permissions, (('basic_access', 'Can access this app'),))


class AccessTokenModelTest(TestCase):
    def setUp(self):
        self.server = Server.objects.create(server=1, name="Test Server", protocol="Discord")
        self.access_token = AccessToken.objects.create(token="abc123", owner=None)

    def test_access_token_str_representation(self):
        self.assertEqual(str(self.access_token), "abc123")

    def test_access_token_servers(self):
        self.assertEqual(self.access_token.servers.count(), 0)


class WebhookModelTest(TestCase):
    def setUp(self):
        self.webhook = Webhook.objects.create(
            url="https://example.com/webhook", name="Test Webhook")

    def test_webhook_str_representation(self):
        self.assertEqual(str(self.webhook), "Test Webhook")

    def test_webhook_send_embed(self):
        # Add test for send_embed method if applicable
        pass


class RelayConfigurationModelTest(TestCase):
    def setUp(self):

        self.server = Server.objects.create(server=1, name="Test Server", protocol="Discord")
        self.channel = Channel.objects.create(channel=1, name="Test Channel", server=self.server)
        self.webhook = Webhook.objects.create(
            url="https://example.com/webhook", name="Test Webhook")
        discordbot_server = AADiscordBotServers.objects.create(server=1, name="Test Server")
        discordbot_channel = AADiscordBotChannels.objects.create(
            channel=1, name="Test Channel", server=discordbot_server)
        self.destination_aadiscordbot = DestinationAADiscordBot.objects.create(
            destination=discordbot_channel, destination_type=DestinationAADiscordBot.Message_Type.CHANNEL_MESSAGE)
        self.relay_config = RelayConfiguration.objects.create(name="Test Relay Configuration")

        self.relay_config.source_servers.add(self.server)
        self.relay_config.source_channels.add(self.channel)
        self.relay_config.destination_webhooks.add(self.webhook)
        self.relay_config.destination_aadiscordbot.add(self.destination_aadiscordbot)

    def test_relay_config_str_representation(self):
        self.assertEqual(str(self.relay_config), "Test Relay Configuration")

    def test_relay_config_source_servers(self):
        self.assertEqual(self.relay_config.source_servers.count(), 1)

    def test_relay_config_source_channels(self):
        self.assertEqual(self.relay_config.source_channels.count(), 1)

    def test_relay_config_destination_webhooks(self):
        self.assertEqual(self.relay_config.destination_webhooks.count(), 1)

    def test_relay_config_destination_aadiscordbot(self):
        self.assertEqual(self.relay_config.destination_aadiscordbot.count(), 1)


class RelaysConfigModelTest(TestCase):
    def setUp(self):
        self.webhook = Webhook.objects.create(
            url="https://example.com/webhook", name="Test Webhook")
        self.relays_config = RelaysConfig.objects.create()

        self.relays_config.status_webhooks.add(self.webhook)

    def test_relays_config_str_representation(self):
        self.assertEqual(str(self.relays_config), "AA Relays Settings")

    def test_relays_config_status_webhooks(self):
        self.assertEqual(self.relays_config.status_webhooks.count(), 1)


class EventModelTest(TestCase):
    def test_event_creation(self):
        # Create a new Event instance
        Event.objects.create(
            event=1,
            name="Test Event",
            description="This is a test event",
            start=timezone.now(),
            end=timezone.now(),
        )

        # Check if the Event was created successfully
        self.assertEqual(Event.objects.count(), 1)

        # Retrieve the Event from the database
        saved_event = Event.objects.get(pk=1)

        # Compare the attributes of the saved Event with the original values
        self.assertEqual(saved_event.name, "Test Event")
        self.assertEqual(saved_event.description, "This is a test event")
